from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from cron_converter import Cron
from fastapi import Depends, Query, status
from sqlalchemy import insert, select, update

from deplio.auth.dependencies import APIKeyAuthCredentials, api_key_auth
from deplio.context import Context, context
from deplio.models.data.head.db.cron import CronInvocation, CronJob, CronJobStatus
from deplio.models.data.head.db.jobs import ScheduledJob, ScheduledJobStatus
from deplio.models.data.head.tables.cron import cron_job_table, cron_invocation_table
from deplio.models.data.head.tables.jobs import scheduled_job_table
from deplio.models.data.head.endpoints.cron import (
    DeleteCronJobResponse,
    GetCronJobsResponse,
    PostCronJobRequest,
    PostCronJobResponse,
)
from deplio.models.data.head.responses import (
    DeplioError,
    error_response,
    generate_responses,
)
from deplio.routers import create_router
from deplio.services.db import DbSessionDependency
from deplio.services.supabase import SupabaseClient, supabase_admin
from deplio.tags import Tags

router = create_router(prefix='/cron')


@router.get(
    '',
    summary='List Deplio Cron jobs',
    description='Get a list of cron jobs that have been set up in Deplio.',
    responses=generate_responses(GetCronJobsResponse),
    tags=[Tags.CRON],
    response_description='List of cron jobs',
    operation_id='cron:list',
)
async def get(
    auth: Annotated[APIKeyAuthCredentials, Depends(api_key_auth)],
    supabase_admin: Annotated[SupabaseClient, Depends(supabase_admin)],
    context: Annotated[Context, Depends(context)],
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 25,
):
    try:
        response = (
            await supabase_admin.table('cron_job')
            .select('*', count='exact')  # type: ignore
            .eq('team_id', auth.team.id)
            .order('created_at', desc=True)
            .is_('deleted_at', 'null')
            .range((page - 1) * page_size, page * page_size)
            .execute()
        )
    except Exception as e:
        print(f'Error getting cron jobs: {e}')
        context.errors.append(DeplioError(message='Failed to get cron jobs'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    if response.count is None:
        context.errors.append(DeplioError(message='Failed to get cron jobs'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    return GetCronJobsResponse(
        cron_jobs=[CronJob(**record) for record in response.data],
        count=len(response.data),
        total=response.count,
        page=page,
        page_size=page_size,
        warnings=context.warnings,
    )


@router.post(
    '',
    summary='Create a new cron job',
    description='Set up a new cron job to execute some work on a schedule',
    responses=generate_responses(PostCronJobResponse),
    tags=[Tags.CRON],
    response_description='The cron job ID and the next invocation time',
)
async def create(
    auth: Annotated[APIKeyAuthCredentials, Depends(api_key_auth)],
    session: DbSessionDependency,
    context: Annotated[Context, Depends(context)],
    cron_job_request: PostCronJobRequest,
):
    cron_job_insert = {
        **cron_job_request.to_insert(),
        'team_id': str(auth.team.id),
        'api_key_id': str(auth.api_key.id),
    }

    try:
        cron_job_result = await session.execute(
            insert(cron_job_table).values(cron_job_insert).returning(cron_job_table)
        )
        cron_job_record = cron_job_result.one()._mapping
    except Exception as e:
        print(f'Error inserting into cron_job: {e}')
        context.errors.append(DeplioError(message='Failed to insert into cron_job'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    cron_job = CronJob(**cron_job_record)

    response = PostCronJobResponse(cron_job_id=cron_job.id, warnings=context.warnings)

    if cron_job.status == CronJobStatus.active:
        # Get next cron invocation time and schedule it
        cron = Cron(cron_job.schedule)
        schedule = cron.schedule(cron_job.created_at)
        next = schedule.next()

        scheduled_job_insert = {
            'api_key_id': str(auth.api_key.id),
            'team_id': str(auth.team.id),
            'status': ScheduledJobStatus.pending,
            'executor': {
                **cron_job.executor.model_dump(),
                'destination': str(cron_job.executor.destination),
            },
            'scheduled_for': next,
            'metadata': cron_job.metadata,
        }

        try:
            result = await session.execute(
                insert(scheduled_job_table)
                .values(scheduled_job_insert)
                .returning(scheduled_job_table)
            )
            scheduled_job_record = result.one()._mapping
        except Exception as e:
            print(f'Error inserting into scheduled_job: {e}')
            context.errors.append(
                DeplioError(message='Failed to insert into scheduled_job')
            )
            return error_response(
                message='Internal server error',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                warnings=context.warnings,
                errors=context.errors,
            )

        scheduled_job = ScheduledJob(**scheduled_job_record)
        response.next_invocation = scheduled_job.scheduled_for

        # Insert cron invocation join record
        cron_invocation_insert = {
            'cron_job_id': str(cron_job.id),
            'scheduled_job_id': str(scheduled_job.id),
            'metadata': cron_job.metadata,
        }

        try:
            await session.execute(
                insert(cron_invocation_table).values(cron_invocation_insert)
            )
        except Exception as e:
            print(f'Error inserting into cron_invocation: {e}')
            context.errors.append(
                DeplioError(message='Failed to insert into cron_invocation')
            )
            return error_response(
                message='Internal server error',
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                warnings=context.warnings,
                errors=context.errors,
            )

    await session.commit()
    return response


@router.delete(
    '/{cron_job_id}',
    summary='Delete a cron job',
    description='Delete a cron job from Deplio. Will also delete any associated scheduled jobs.',
    responses=generate_responses(DeleteCronJobResponse),
    tags=[Tags.CRON],
)
async def delete(
    auth: Annotated[APIKeyAuthCredentials, Depends(api_key_auth)],
    session: DbSessionDependency,
    context: Annotated[Context, Depends(context)],
    cron_job_id: UUID,
):
    try:
        response = await session.execute(
            update(cron_job_table)
            .where(
                cron_job_table.c.id == cron_job_id,
                cron_job_table.c.team_id == auth.team.id,
                cron_job_table.c.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.now(UTC))
            .returning(cron_job_table.c.id)
        )
        cron_delete_response = response.all()
    except Exception as e:
        print(f'Error deleting cron job: {e}')
        context.errors.append(DeplioError(message='Failed to delete cron job'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    if len(cron_delete_response) == 0:
        return error_response(
            message='Cron job not found',
            status_code=status.HTTP_404_NOT_FOUND,
            warnings=context.warnings,
            errors=context.errors,
        )

    try:
        response = await session.execute(
            select(cron_invocation_table).where(
                cron_invocation_table.c.cron_job_id == cron_job_id
            )
        )
        cron_invocations = [CronInvocation(**record) for record in response.mappings()]
    except Exception as e:
        print(f'Error fetching cron invocations: {e}')
        context.errors.append(DeplioError(message='Failed to fetch cron invocations'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    try:
        response = await session.execute(
            update(scheduled_job_table)
            .where(
                scheduled_job_table.c.id.in_(
                    [
                        cron_invocation.scheduled_job_id
                        for cron_invocation in cron_invocations
                    ]
                ),
                scheduled_job_table.c.started_at.is_(None),
            )
            .values(deleted_at=datetime.now(UTC))
            .returning(scheduled_job_table.c.id)
        )
        scheduled_job_ids: list[UUID] = list(response.scalars().all())
    except Exception as e:
        print(f'Error deleting scheduled jobs: {e}')
        context.errors.append(DeplioError(message='Failed to delete scheduled jobs'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    try:
        await session.execute(
            update(cron_invocation_table)
            .where(cron_invocation_table.c.scheduled_job_id.in_(scheduled_job_ids))
            .values(deleted_at=datetime.now(UTC))
        )
    except Exception as e:
        print(f'Error deleting cron invocations: {e}')
        context.errors.append(DeplioError(message='Failed to delete cron invocations'))
        return error_response(
            message='Internal server error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            warnings=context.warnings,
            errors=context.errors,
        )

    await session.commit()
    return DeleteCronJobResponse(
        cron_job_id=cron_job_id,
        scheduled_job_ids=scheduled_job_ids,
        warnings=context.warnings,
    )
