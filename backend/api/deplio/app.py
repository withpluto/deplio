from fastapi.routing import APIRoute
from deplio.models.versions import version_bundle
from deplio.config import settings
from deplio.routes.q import router as q_router
from deplio.routes.version import router as version_router
from deplio.tags import tags_metadata
from fastapi.middleware import Middleware
from cadwyn import Cadwyn
from deplio.middleware.default_version import DefaultVersioningMiddleware


def generate_openapi_id(route: APIRoute) -> str:
    print(route)
    if not route.tags:
        return route.name
    return f'{str(route.tags[0]).lower().replace(' ', '_')}:{route.name}'


app = Cadwyn(
    title='Deplio',
    summary='Simple utils for serverless applications',
    docs_url=None,
    redoc_url='/docs',
    version=settings.current_version.isoformat(),
    versions=version_bundle,
    api_version_header_name=settings.version_header,
    middleware=[
        Middleware(
            DefaultVersioningMiddleware,
            api_version_var=version_bundle.api_version_var,
            latest_version=settings.current_version,
        ),
    ],
    openapi_tags=tags_metadata,
    servers=[{'url': 'https://api.depl.io'}],
    generate_unique_id_function=generate_openapi_id,
)


app.generate_and_include_versioned_routers(version_router, q_router)
