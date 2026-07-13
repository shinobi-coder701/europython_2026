import { defineAppSetup } from '@slidev/types'

function updateCodeHighlightIndents() {
  const lines = document.querySelectorAll<HTMLElement>('.shiki .line, .slidev-code .line')

  for (const line of lines) {
    const indent = line.textContent?.match(/^ */)?.[0].length ?? 0
    line.style.setProperty('--code-indent-ch', indent.toString())
  }
}

export default defineAppSetup(({ router }) => {
  router.afterEach(() => {
    requestAnimationFrame(updateCodeHighlightIndents)
  })

  window.addEventListener('resize', updateCodeHighlightIndents)

  const observer = new MutationObserver(() => {
    requestAnimationFrame(updateCodeHighlightIndents)
  })

  requestAnimationFrame(() => {
    updateCodeHighlightIndents()
    observer.observe(document.body, {
      subtree: true,
      attributes: true,
      attributeFilter: ['class'],
    })
  })
})
