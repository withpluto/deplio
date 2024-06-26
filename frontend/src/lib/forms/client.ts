import {
  superForm,
  type FormOptions,
  type SuperForm,
} from 'sveltekit-superforms/client'
import type { SuperValidated, ZodValidation } from 'sveltekit-superforms'
import type { AnyZodObject } from 'zod'
import type { ToastStore, ToastSettings } from '@skeletonlabs/skeleton'

export type FormMessage = {
  status: 'error' | 'success'
  message: string
}

export const displayToast = (
  formMessage: FormMessage,
  toastStore: ToastStore,
  settings?: ToastSettings,
) => {
  const t: ToastSettings = {
    message: formMessage.message,
    background:
      formMessage.status === 'error'
        ? 'variant-filled-error'
        : 'variant-filled-success',
  }
  toastStore.trigger({ ...t, ...settings })
}

export const createForm = <
  T extends ZodValidation<AnyZodObject>,
  M extends FormMessage = FormMessage,
>(
  form: SuperValidated<T, M>,
  toastStore: ToastStore,
  options?: FormOptions<T, M>,
): SuperForm<T> => {
  const onUpdated: (event: {
    form: Readonly<SuperValidated<AnyZodObject, M>>
  }) => unknown = async ({ form }) => {
    if (form.message) {
      displayToast(form.message, toastStore)
    }
    if (options?.onUpdated) {
      await options.onUpdated({ form })
    }
  }

  // Remove onUpdated from options so it doesn't override our custom handler
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { onUpdated: useless, ...opts } = options ?? {}

  return superForm(form, {
    taintedMessage: 'You have unsaved changes. Are you sure you want to leave?',
    multipleSubmits: 'prevent',
    delayMs: 500,
    onUpdated,
    ...opts,
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } as any)
}
