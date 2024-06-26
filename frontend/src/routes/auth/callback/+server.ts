import { extractRedirectUrl } from '$lib/utils'
import type { RequestHandler } from '@sveltejs/kit'
import { redirect } from '@sveltejs/kit'

export const GET: RequestHandler = async ({ url, locals: { supabase } }) => {
  const code = url.searchParams.get('code')

  if (code) {
    await supabase.auth.exchangeCodeForSession(code)
  }

  throw redirect(303, extractRedirectUrl(url, '/'))
}
