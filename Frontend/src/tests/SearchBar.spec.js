import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import SearchBar from '../components/SearchBar.vue'

describe('SearchBar.vue', () => {
  it('renders correctly with default props', () => {
    const wrapper = mount(SearchBar)
    const input = wrapper.find('input')
    
    expect(input.exists()).toBe(true)
    expect(input.attributes('placeholder')).toBe('Search jobs, companies, or keywords...')
    expect(input.element.value).toBe('')
  })

  it('renders with provided modelValue', () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: 'Developer'
      }
    })
    const input = wrapper.find('input')
    
    expect(input.element.value).toBe('Developer')
  })

  it('emits update:modelValue when input changes', async () => {
    const wrapper = mount(SearchBar, {
      props: {
        modelValue: ''
      }
    })
    const input = wrapper.find('input')
    
    await input.setValue('Vue 3')
    
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['Vue 3'])
  })
})
