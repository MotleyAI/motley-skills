# HTML Presentation Template (Body-Only Mode)

You generate **only the slide `<section>` elements**. The server wraps them with DOCTYPE, `<head>`, CSS, JS, fonts, logos, and chrome.

## CRITICAL: No Inline Styles

All visual styling comes from CSS classes defined in the BrandConfig's `css_block` fields. The server injects these automatically. **NEVER add inline `style=` attributes** for colors, fonts, padding, borders, alignment, or sizing. The ONLY exception is `transition-delay` for animation stagger timing.

Use the CSS class names from the BrandConfig's `html_template` and `css_block` fields. If a class like `.data-table`, `.dtbl`, `.metric-card`, `.chart-container` exists in the css_block, USE IT — don't reinvent the styling inline.

## Body HTML Structure

```html
<!-- Slide 1: Title (first_slide_type from BrandConfig) -->
<section class="slide slide-title" id="slide-1">
  <div class="logo on-light rv"><!-- logo --></div>
  <div class="slide-content" style="justify-content: center;">
    <div class="accent-bar rv"></div>
    <h1 class="rv">Presentation Title</h1>
    <p class="subtitle rv" style="transition-delay:0.1s">Subtitle or author</p>
  </div>
</section>

<!-- Slide 2: Content -->
<section class="slide slide-content-default" id="slide-2">
  <div class="topbar">
    <div class="logo on-light rv"><!-- logo --></div>
    <span class="pg-num rv">02 / 07</span>
  </div>
  <div class="s-hdr rv">
    <span class="accent-bar"></span>
    <span class="s-title">Section Title</span>
  </div>
  <div class="content-body">
    <p class="rv">Content goes here...</p>
    <ul>
      <li class="rv" style="transition-delay:0.1s">First point</li>
      <li class="rv" style="transition-delay:0.2s">Second point</li>
    </ul>
  </div>
</section>

<!-- Slide 3: Data with chart -->
<section class="slide slide-data" id="slide-3">
  <div class="topbar" style="position:relative;z-index:1;">
    <div class="logo on-light rv"><!-- logo --></div>
    <span class="pg-num rv">03 / 07</span>
  </div>
  <div class="s-hdr rv" style="position:relative;z-index:1;">
    <span class="accent-bar"></span>
    <span class="s-title">Monthly Trend</span>
  </div>
  <div class="content-body" style="position:relative;z-index:1;">
    <div id="chart-1" class="chart-container rv" data-chart-block="monthly_trend"></div>
  </div>
</section>

<!-- Slide N: Closing (last_slide_type from BrandConfig) -->
<section class="slide slide-closing" id="slide-7">
  <div class="logo on-dark rv" style="margin-bottom: 2rem;"><!-- logo --></div>
  <div class="cl-title rv">Thank You</div>
  <div class="cl-sub rv" style="transition-delay:0.1s">Subtitle</div>
</section>
```

## Key Conventions

### Markers (Server Replaces These)

| Marker | Where | Server Action |
|--------|-------|--------------|
| `<!-- logo -->` | Inside `<div class="logo VARIANT rv">` | Injects brand SVG logo |
| `<!-- wave -->` | Inside `<div class="wave">` | Generates wave footer SVG |
| `<!-- footer-text -->` | Where footer text should appear | Injects footer text |

### Animation Classes

Apply these from the BrandConfig's `animations.presets`:

| Class | Effect |
|-------|--------|
| `.rv` | Fade + slide up (translateY) |
| `.rv-l` | Fade + slide from left (translateX) |
| `.rv-r` | Fade + slide from right (translateX) |

Stagger with inline `transition-delay`:
```html
<p class="rv" style="transition-delay:0.1s">First</p>
<p class="rv" style="transition-delay:0.2s">Second</p>
```

### CSS Classes from BrandConfig

Use `css_class` from `slide_types.types` on each `<section>`. Use class names from `html_template` for inner elements. The server injects all CSS that makes these classes work.

### Chart Containers

Every chart container **must** have:
- A unique `id` attribute
- A `data-chart-block="BLOCK_NAME"` attribute
- The `chart-container` class

## Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Chart slide | 1 heading + 1 chart container + optional caption |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

## What You Do NOT Include

- No `<!DOCTYPE>`, `<html>`, `<head>`, `<body>` tags
- No `<style>` blocks
- No `<script>` blocks
- No font `<link>` tags
- No CDN scripts
- No logo SVG markup
- No viewport-base.css
- No chart initialization code
