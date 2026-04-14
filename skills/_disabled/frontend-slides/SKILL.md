---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. Helps non-designers discover their aesthetic through visual exploration rather than abstract choices.
---

# Frontend Slides

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |
| Chart slide | 1 heading + 1 chart (max 60vh height) + optional caption |
| Table slide | 1 heading + 1 table container + optional caption |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.

---

## Phase 1: Content Discovery (New Presentations)

**Ask ALL questions in a single AskUserQuestion call** so the user fills everything out at once:

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 4 — Inline Editing** (header: "Editing"):
Do you need to edit text directly in the browser after generation? Options:
- "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
- "No" — Presentation only, keeps file smaller

**Remember the user's editing choice — it determines whether edit-related code is included in Phase 3.**

If user has content, ask them to share it.

### Step 1.2: Image Evaluation (if images provided)

If user selected "No images" → skip to Phase 2.

If user provides an image folder:
1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **View each image** — Use the Read tool (Claude is multimodal)
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm via AskUserQuestion** (header: "Outline"): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.

---

## Phase 2: Load Brand Style

Call `list_resources(what="styles")` to see available styles. If multiple exist, ask the user which to use. Then call `read_style(style_name=chosen_name)` — the response is a slim BrandConfig with only the semantic metadata you need (no CSS, JS, or SVG).

The slim BrandConfig tells you:
- **Slide types** (`payload.slide_types.types`): available slide archetypes with `html_template`, `layout_description`, `when_to_use`, `css_class`. First slide must use `first_slide_type`, last must use `last_slide_type`.
- **Colors** (`payload.colors.tokens`): named color tokens with values and usage descriptions.
- **Animations** (`payload.animations.presets`): available animation classes (e.g. `.rv`, `.rv-l`) and stagger delay. Respect `forbidden_effects`.
- **Decorative elements** (`payload.decorative_elements`): HTML templates for brand motifs, with `applies_to_slide_types`.
- **Footer** (`payload.footer.kind`): `"text"`, `"svg_wave"`, or `"none"`.
- **Chrome** (`payload.chrome`): boolean flags for progress bar, nav dots, topbar.
- **Typography**: font family names (for reference, not for embedding).
- **Forbidden patterns**: visual patterns to avoid.

**You do NOT need to handle CSS, JS, fonts, logos, or viewport-base.css.** The server injects all of that when you call `save_html`.

---

## Phase 3: Generate Body HTML

Generate **body-only HTML** — just the slide `<section>` elements. The server handles all CSS, JS, fonts, logos, and chrome.

### CRITICAL: Use Brand CSS Classes, NEVER Inline Styles

The BrandConfig's `css_block` fields define all the CSS classes you need. The server injects these CSS rules automatically. **You MUST use these classes and NEVER add inline `style=` attributes for visual styling.**

**Rules:**
- **NEVER** add inline `style=` for colors, fonts, padding, borders, alignment, or sizing
- **NEVER** hardcode hex colors (e.g. `style="color: #016FFF"`) — the CSS classes handle all colors
- **NEVER** wrap elements in extra `<div style="position:relative;z-index:1;">` containers
- **Tables** MUST use the brand's table class (`.data-table`, `.dtbl`, etc.) from the css_block — no inline table styling. Apply cell classes (`.n`, `.hi`, `.dim`) consistently to ALL rows, not just the first.
- **Charts** MUST use `class="chart-container"` with no inline width/height
- **Logos** MUST use `<!-- logo -->` marker inside `<div class="logo VARIANT">` — never paste SVG inline or leave the div empty
- The ONLY acceptable inline styles are `transition-delay` for animation stagger timing

**Read the `css_block` fields** in the BrandConfig to see exactly what CSS classes are available for each slide type.

### What You Generate

Use the `html_template` patterns from the BrandConfig to structure each slide:

```html
<section class="slide slide-title" id="slide-1">
  <div class="logo on-light rv"><!-- logo --></div>
  <div class="slide-content">
    <div class="accent-bar rv"></div>
    <h1 class="rv">Presentation Title</h1>
    <p class="subtitle rv" style="transition-delay:0.1s">Subtitle</p>
  </div>
</section>

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
    <p class="rv">Content here...</p>
  </div>
</section>
```

### Marker Convention

The server replaces these markers with actual content:

- **`<!-- logo -->`** inside a `<div class="logo VARIANT rv">` — server injects the brand's SVG logo
- **`<!-- wave -->`** inside a `<div class="wave">` — server generates wave footer SVGs with unique gradient IDs
- **`<!-- footer-text -->`** — server injects footer text content

**CRITICAL — Logos: NEVER look up, extract, fetch, or paste actual logo SVG markup.** You do not need the SVG. Just write the HTML comment marker `<!-- logo -->` inside a container div. The server has the logo and injects it automatically. Example:
```html
<div class="evalart-logo reveal"><!-- logo --></div>
```
That is ALL you write. Do not call any tools to get the logo. Do not read any files to find the logo. Do not inline any `<svg>` elements. Just the marker comment.

### Charts

**NEVER generate chart data, chart options, or chart rendering code.** Place chart containers that reference the source document's chart blocks:

```html
<div id="chart-1" class="chart-container rv" data-chart-block="BLOCK_NAME"></div>
```

The `data-chart-block` attribute is **required** on every chart container. The server fetches the chart config from the source document and generates all initialization code.

### Tables

**NEVER generate table data or `<table>` markup.** Place table containers that reference the source document's table blocks:

```html
<div id="table-1" class="table-container rv" data-table-block="BLOCK_NAME"></div>
```

The `data-table-block` attribute is **required** on every table container. The server fetches the table data from the source document and generates the styled `<table>` element using the brand's `table_css_class`.

### What You Do NOT Generate

- No `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` tags
- No `<style>` blocks — all CSS is injected server-side
- No `<script>` blocks — all JS is injected server-side
- No font loading `<link>` tags
- No viewport-base.css content
- No echarts_config.min.js
- No logo SVG markup (use `<!-- logo -->` marker)

### What You Still Handle

- Content splitting across slides (respect density limits)
- Slide type selection (using `css_class` from the BrandConfig)
- Animation class assignment (`.rv`, `.rv-l`, `.rv-r`) with stagger delays via `transition-delay` inline styles
- HTML structure following `html_template` patterns
- Content density limits (same rules as before)

**Before generating, read:**
- [html-template.md](html-template.md) — Body-only template reference
- [animation-patterns.md](animation-patterns.md) — Animation class reference
- [charting.md](charting.md) — Chart container reference (if presentation includes charts)
- [tabling.md](tabling.md) — Table container reference (if presentation includes tables)

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Save & share** — Call `save_html(html_content=<body HTML>, style_name=<chosen style>, document_id=<source doc ID>, title="Presentation Title", filename="presentation-name.html")` to enrich and upload the presentation. Note the `html_id` from the response for potential PDF conversion.
2. **Summarize** — Tell the user:
   - Shareable HTML URL, style name, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
3. **Offer PDF** — Ask if the user would also like a PDF version. If yes, call `html_to_pdf(html_id=<the html_id from step 1>)` — this reuses the already-saved HTML without re-uploading it. Share the returned PDF URL with the user.

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [html-template.md](html-template.md) | Body-only HTML structure reference | Phase 3 (generation) |
| [animation-patterns.md](animation-patterns.md) | Animation class reference and effect-to-feeling guide | Phase 3 (generation) |
| [charting.md](charting.md) | Chart container reference (data-chart-block convention) | Phase 3 (when presentation includes charts) |
| [tabling.md](tabling.md) | Table container reference (data-table-block convention) | Phase 3 (when presentation includes tables) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (conversion) |
