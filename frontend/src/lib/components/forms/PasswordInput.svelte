<script lang="ts">
  import type { Variant } from '$lib/types/styling'
  import TextInput from './TextInput.svelte'

  export let id: string
  export let name: string | null = null
  export let variant: Variant | null = null
  export let label: string | null = null
  export let placeholder: string | null = null
  /**
   * String array of errors to display
   */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  export let errors: any = [] as string[]
  export let minlength: number | null = null
  export let maxlength: number | null = null
  export let required = false
  export let disabled = false
  export let readonly = false
  export let autocomplete: HTMLInputElement['autocomplete'] | null = 'current-password'
  export let pattern: RegExp | null = null
  export let value: string

  let classes = ''
  export { classes as class }

  $: errors = errors as string[]
</script>

<TextInput
  type="password"
  bind:value
  class={classes}
  {variant}
  {label}
  {id}
  {name}
  {placeholder}
  {minlength}
  {maxlength}
  {required}
  {disabled}
  {readonly}
  {autocomplete}
  {pattern}
  {errors}
/>
