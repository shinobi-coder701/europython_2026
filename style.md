# Slide Style Rules

This deck follows the readability target from the past PyCon US slide audit:

| Reference deck | Body min / avg | Code min / avg |
| --- | ---: | ---: |
| PyCon US 2025 | 29.9 / 36.5px | 26.5 / 31.0px |
| PyCon US 2024 | 31.3 / 34.4px | 19.1 / 29.8px |
| PyCon JP 2025 | 20.0 / 29.2px | 21.6 / 22.3px |

PDF extraction from the public PyCon US 2024/2025 decks also shows that code
is usually larger than the minimum:

| Reference PDF | Non-code median / avg | Code median / avg |
| --- | ---: | ---: |
| PyCon US 2025 PDF | 37.3 / 36.1px | 29.3 / 30.1px |
| PyCon US 2024 PDF | 32.0 / 33.6px | 29.3 / 27.9px |

## Typography

- Cover title: 64px, 900 weight.
- Slide title: 48px minimum for `h2`, 56px for `h1`.
- Section number and section title: 52px, same baseline, no wrapping.
- Body text and bullets: 32px minimum, 700 weight.
- About Me bullets: 30px minimum because the slide intentionally carries more content.
- Notes and labels: about 32px. Do not use notes as body-copy substitutes.
- Tables: 24px standard. Dense tables at 21px are allowed only as a last resort and must be reviewed; prefer splitting a slide.
- QR URL labels: 12px exception only. They are secondary labels beside machine-readable QR codes.
- Inline code inherits the surrounding text size. `compact-code` and `mini-code` must never shrink inline code in headings, bullets, notes, or tables.

## Code

- Standard code: 28px target, close to the PyCon US 2024/2025 code median of 29.3px.
- Compact code: 28px target with tighter line-height; do not use compact code as a font-size reduction.
- Mini code: 20px minimum, only if splitting cannot preserve the example and the slide is explicitly reviewed.
- Do not reduce code size to fix overflow. Split code, shorten comments, wrap lines, or split slides.
- For side-by-side comparison slides, first try a code-focused layout such as `code-compare` and keep code at 28px.
- Code focus uses v-click line highlighting: first show plain code, then reveal red outlines one step at a time or by meaningful units.
- Focus outlines must not dim non-focused code.
- Focus outlines must start at the first visible character, not at indentation whitespace.

## Color And Contrast

- Background: white.
- Primary text: `#0f172a`.
- Secondary text: `#1f2937`.
- Link text: `#0369a1`.
- Inline code: `#166534`, bold.
- Code background: `#f3f4f6`.
- Accent / focus outline: `#dc2626`.
- Avoid low-opacity text. Hidden v-click states may fade, but visible content must render at full opacity.

## Layout

- 1920x1080 full expansion must have no vertical overflow, horizontal overflow, or code scroll.
- Prefer 2-4 main bullets per slide.
- If a slide needs smaller text to fit, split the slide instead.
- Tables with more than four dense rows should be split unless all text remains at 24px or larger.
- Keep white background, high contrast, top-left bold titles, and generous whitespace consistent with the PyCon US 2024/2025 style.

## Current Audit Command

Run the rendered audit at 1920x1080 with all clicks expanded after any layout change:

```bash
npx slidev build --base /europython_2026/
```

Then verify in browser automation:

- no visible non-QR text below 23px;
- no body/list text below 30px;
- no table text below 24px unless explicitly approved;
- no code below 28px unless the slide is explicitly marked and reviewed as `mini-code`;
- no dimmed visible code;
- no overflow or code scroll at `?clicks=99`.
