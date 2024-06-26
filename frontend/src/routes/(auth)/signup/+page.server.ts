import { emailSignupFormSchema, providerAuthFormSchema } from '$lib/forms/auth'
import { get_supabase_admin_client } from '$lib/utils.server'
import { fail, redirect } from '@sveltejs/kit'
import { message, setError, superValidate } from 'sveltekit-superforms/server'
import type { Actions, PageServerLoad } from './$types'
import { PUBLIC_DEPLIO_URL } from '$env/static/public'

export const load: PageServerLoad = async (event) => {
  const emailSignupForm = await superValidate(event, emailSignupFormSchema)
  const providerAuthForm = await superValidate(event, providerAuthFormSchema)
  return { emailSignupForm, providerAuthForm }
}

export const actions: Actions = {
  emailSignup: async ({ request, locals: { supabase } }) => {
    const form = await superValidate(request, emailSignupFormSchema)

    if (!form.valid) {
      return fail(400, { form })
    }

    const supabaseAdmin = get_supabase_admin_client()
    // Check if username is already taken
    const { data: usernameData, error: usernameError } = await supabaseAdmin
      .from('user')
      .select('id')
      .eq('username', form.data.username)
      .maybeSingle()

    if (usernameError) {
      console.log(usernameError)
      return message(
        form,
        {
          status: 'error',
          message: 'There was an error signing you up. Please try again later.',
        },
        { status: 500 },
      )
    }

    if (usernameData) {
      return setError(form, 'username', 'This username is already in use.')
    }

    const { error: authError } = await supabase.auth.signUp({
      email: form.data.email,
      password: form.data.password,
      options: {
        emailRedirectTo: `${PUBLIC_DEPLIO_URL}/auth/callback?redirectUrl=/dashboard`,
        data: {
          username: form.data.username,
        },
      },
    })

    if (authError) {
      if (authError.message === 'User already registered') {
        return setError(form, 'email', 'This email is already in use.')
      }
      console.log(authError)
      return message(
        form,
        {
          status: 'error',
          message: 'There was an error signing you up. Please try again later.',
        },
        { status: 500 },
      )
    }

    throw redirect(303, '/signup/verify')
  },
}
