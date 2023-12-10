import { PUBLIC_SUPABASE_URL, PUBLIC_SUPABASE_ANON_KEY } from '$env/static/public'
import { createSupabaseServerClient } from '@supabase/auth-helpers-sveltekit'
import type { Handle } from '@sveltejs/kit'
import { error, redirect } from '@sveltejs/kit'
import { cache } from '$lib/cache'
import type { TeamWithRole, UserWithTeams } from '$lib/types/supabase'

export const handle: Handle = async ({ event, resolve }) => {
  event.locals.supabase = createSupabaseServerClient({
    supabaseUrl: PUBLIC_SUPABASE_URL,
    supabaseKey: PUBLIC_SUPABASE_ANON_KEY,
    event,
  })

  /**
   * a little helper that is written for convenience so that instead
   * of calling `const { data: { session } } = await supabase.auth.getSession()`
   * you just call this `await getSession()`
   */
  event.locals.getSession = async () => {
    const {
      data: { session },
    } = await event.locals.supabase.auth.getSession()
    return session
  }
  const session = await event.locals.getSession()

  if (event.url.pathname.startsWith('/dashboard') && !session) {
    if (!session) {
      throw redirect(303, '/login')
    }
  } else if (!session) {
    return resolve(event, {
      filterSerializedResponseHeaders(name) {
        return name === 'content-range'
      },
    })
  }

  let user = await cache.hgetall(`user:${session?.user.id}`)
  const refreshCache = event.url.searchParams.get('refreshCache')

  if (!user || refreshCache) {
    const { data: userFetch, error: userFetchError } = await event.locals.supabase
      .from('user')
      .select('*, team_user (team (*), role)')
      .eq('user_id', session?.user.id)
      .single()

    if (userFetchError) {
      throw error(500, `Error fetching user: ${userFetchError.message}`)
    }

    if (!userFetch) {
      throw error(404, 'User not found')
    }

    const { team_user: teamUser, ...extractedUser } = userFetch

    const earliestTeam = teamUser.sort((teamUser1, teamUser2) => {
      return (teamUser1?.team?.created_at ?? 0) < (teamUser2?.team?.created_at ?? 0)
        ? -1
        : 1
    })[0]?.team

    if (!earliestTeam) {
      throw error(404, 'User not found')
    }

    const userWithTeams: UserWithTeams = {
      ...extractedUser,
      currentTeamId: earliestTeam.id,
      teams: teamUser.map((teamWithRole) => {
        if (!teamWithRole.team) {
          throw error(404, 'Team not found')
        }
        return {
          id: teamWithRole.team.id,
          name: teamWithRole.team.name,
          type: teamWithRole.team.type,
          avatar_url: teamWithRole.team.avatar_url,
          role: teamWithRole.role,
        }
      }),
    }

    await cache.hset(`user:${session?.user.id}`, userWithTeams, {
      ttlSeconds: 60 * 60, // 1 hour
    })
    user = userWithTeams
  }
  event.locals.user = user

  const newTeamId = event.url.searchParams.get('team')

  if (newTeamId) {
    event.locals.user.currentTeamId = newTeamId
    cache.hset(`user:${session?.user.id}`, event.locals.user, {
      ttlSeconds: 60 * 60, // 1 hour
    })
  }

  event.locals.team = event.locals.user.teams.find(
    (team) => team.id === event.locals.user.currentTeamId,
  ) as TeamWithRole

  return resolve(event, {
    filterSerializedResponseHeaders(name) {
      return name === 'content-range'
    },
  })
}
