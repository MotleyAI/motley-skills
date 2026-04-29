---
name: frontend-slides
description: Create stunning, animation-rich HTML presentations locked to your brand identity. Use when the user wants to build a branded presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch. On first use, a brand wizard walks you through defining your visual identity — every presentation after that is automatically on-brand.
---

# Branded Frontend Slides

Create zero-dependency, animation-rich HTML presentations locked to your brand identity.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Brand-Locked** — Every presentation uses your brand's colors, fonts, logo, and visual signature. No style picker, no generic themes.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted for your brand.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight — within the brand's visual identity.

Focus on:

- Typography: Use the brand's chosen fonts. Vary weights and sizes for hierarchy.
- Color & Theme: Commit to the brand palette. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- Motion: Use animations for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth using brand colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the brand's signature elements.

Avoid generic AI-generated aesthetics:

- Overused font families (Inter, Roboto, Arial, system fonts) — unless the brand specifically chose them
- Cliched color schemes (particularly purple gradients on white)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

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

| Slide Type    | Maximum Content                                           |
| ------------- | --------------------------------------------------------- |
| Title slide   | 1 heading + 1 subtitle + optional tagline                 |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid  | 1 heading + 6 cards maximum (2x3 or 3x2)                  |
| Code slide    | 1 heading + 8-10 lines of code                            |
| Quote slide   | 1 quote (max 3 lines) + attribution                       |
| Image slide   | 1 heading + 1 image (max 60vh height)                     |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

**First: check if [BRAND_CONFIG.md](BRAND_CONFIG.md) exists and is filled in** (not just the empty template with `<!-- ... -->` placeholders).

- **No brand config** → Go to Phase 2 (Brand Wizard) before anything else.
- **Brand config exists** → Read it and proceed.

Then determine what the user wants:

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

If user selected "No images" -> skip to Phase 3.

If user provides an image folder:

1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **View each image** — Use the Read tool (Claude is multimodal)
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots -> 3 feature slides, 1 logo -> title/closing slide)
5. **Confirm via AskUserQuestion** (header: "Outline"): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

---

## Phase 2: Brand Wizard

**This phase runs once** — when `BRAND_CONFIG.md` does not exist or is empty/unfilled. It creates the brand configuration that locks every future presentation to the user's visual identity.

### Step 2.0: Brand Input

Ask how they want to define their brand (header: "Brand Setup"). **The recommended path is "From an existing presentation"** — most companies already have a deck template that codifies their visual identity (colors, fonts, logo, layout patterns) far more completely than any website does. Make this the first option and label it `(Recommended)`.

- "From an existing presentation (Recommended)" — Extract brand from a PPT/HTML file they already use
- "From a website" — Extract the design system from a URL using [dembrandt](https://github.com/dembrandt/dembrandt)
- "From brand guidelines" — User provides a PDF, image, or description of their brand
- "From scratch" — Walk through each choice step by step

**Why presentation-first:** A deck template includes pre-resolved decisions (logo placement, slide layouts, color hierarchy, font weights for hero vs body) that a website does not. Websites optimize for scrolling and conversion; decks optimize for the same medium we're generating. Use this as the default unless the user specifically asks for one of the other paths.

### Step 2.1: Gather Brand Identity

**If "From an existing presentation" (recommended path):**

1. Ask for the file. For .pptx, run `python scripts/extract-pptx.py` to extract content, then read the theme XML directly to get the full color scheme, font scheme, and embedded images.
2. **When extracting logos from a PPTX**, list ALL unique embedded images and their pixel dimensions — pick the highest-resolution variant (the wordmark is usually wider, e.g., ~889x269px; the monogram is ~177x137px). Read each candidate image visually before choosing. Embed the chosen logo as a base64 data URI in the brand config.
3. **Verify base64 integrity before saving.** Decode the base64 and check the resulting bytes are a valid PNG/JPEG (PNG signature: `89504e470d0a1a0a`). Headless Chromium fails silently on corrupted images during PDF export — even if interactive Chrome appears to render them. If `<img>.naturalWidth === 0` after load, the encoding is corrupt; re-encode from the source file.
4. **Single-color logos:** if the user only has one color variant (e.g., a black PNG) but needs it on both light and dark slides, use CSS `filter: brightness(0) invert(1)` to render it white on dark backgrounds — no need for a separate white asset.
5. Present what you found and ask the user to confirm or adjust.

**If "From a website":**

This path uses [dembrandt](https://github.com/dembrandt/dembrandt) — a tool that extracts a website's full design system (colors, typography, logo, borders, components) into design tokens in seconds.

1. Ask the user for the URL.

2. **Prefer the dembrandt MCP server if it's connected** (tools named `get_brand_identity`, `get_color_palette`, `get_typography`, `get_design_tokens`, `get_component_styles`, `get_surfaces`, `get_spacing`). Call `get_brand_identity` first for the high-level summary, then `get_color_palette` and `get_typography` for the specifics.

   If the MCP server is not connected, tell the user once: _"I can extract richer brand data if you connect the dembrandt MCP server. To enable it, run: `claude mcp add --transport stdio dembrandt -- npx -y dembrandt-mcp` — but I'll proceed with the CLI now."_

3. **CLI fallback:** Run `npx -y dembrandt <url> --json-only` via Bash and parse the resulting JSON. If the site is JavaScript-heavy or behind Cloudflare, retry with `--slow` or `--browser=firefox`.

4. From the extracted tokens, populate:
   - **Colors:** primary background, primary text, accent (look for the most-used non-neutral hue), and any secondary accents
   - **Typography:** display + body fonts, with the import URL (Google Fonts or Fontshare)
   - **Logo:** if dembrandt returns a logo URL, fetch the image and embed as a base64 data URI in the brand config (URLs break offline)
   - **Feeling:** infer from the palette and typography (e.g., dark + sans-serif + neon = "innovative, bold")

5. **Watch for web-vs-deck font mismatches.** A company's website often uses a commercial display font (e.g. "Factor A" via Adobe Fonts) that isn't on Google Fonts. If the user also has a deck template, ask whether they want the website's font (which may need a paid license) or the deck's font (which is usually already a Google Font). Suggest the closest free Google Fonts equivalent if needed.

6. Present what was extracted and ask the user to confirm or adjust each piece via AskUserQuestion.

**If "From brand guidelines":**

1. Ask the user to share the file
2. Read it and extract: color palette, typography, logo, visual principles
3. Present what you extracted and ask the user to confirm or adjust

**If "From scratch":**

Ask these questions in a single AskUserQuestion call:

- **Company name** (header: "Company"): text input
- **Logo** (header: "Logo"): "I'll paste/upload a logo" / "I don't have one yet"
- **Color mood** (header: "Colors"): Dark & bold / Light & clean / Colorful & energetic / Minimal & muted / "I have specific hex codes"
- **Feeling** (header: "Feeling", multiSelect: true, max 2): Confident & trustworthy / Innovative & bold / Calm & focused / Playful & approachable

### Step 2.2: Choose Typography

Based on the brand mood and feeling, propose 2-3 font pairings (display + body). Use fonts from Google Fonts or Fontshare — never system fonts. Show the font names, weights, and a brief description of why they fit.

Ask the user to pick one, or suggest their own.

### Step 2.3: Design Signature Elements

Based on everything gathered, propose 3 signature visual elements that will make the brand's slides distinctive. These are CSS-only patterns — no illustrations, no stock images. Examples:

- Thick accent bar on left edge of content slides
- Gradient mesh backgrounds with radial overlays in brand colors
- Floating geometric shapes (circles, lines) with brand accent
- Corner decorations using brand pattern
- Halftone dot overlay
- Diagonal split layouts with brand colors

Present the 3 proposals and let the user pick, modify, or request alternatives.

### Step 2.4: Generate Preview

Generate a single title slide as an HTML file (`.claude-design/brand-preview.html`) that demonstrates the full brand identity: logo, colors, fonts, signature elements, and animations. Open it for the user.

Ask (header: "Brand Preview"):
"Does this look right for your brand?" Options: Looks great / Adjust colors / Adjust fonts / Adjust layout / Start over

Iterate until the user approves.

### Step 2.5: Save Brand Config

Once approved, write the final brand configuration to [BRAND_CONFIG.md](BRAND_CONFIG.md) with all values filled in:

- Company name, tagline, website
- Logo (inline SVG or base64 data URI — never a URL that could break)
- Full CSS color palette
- Typography with font import URL
- Theme mode and feeling
- Signature elements with descriptions
- Slide type layouts (title, section, content, metrics, closing)

Delete `.claude-design/brand-preview.html` after saving.

Tell the user: "Your brand is saved. Every presentation from now on will use this identity. To change it later, just ask me to update the brand config."

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 and brand identity from [BRAND_CONFIG.md](BRAND_CONFIG.md).

**Before generating, read these files:**

- [BRAND_CONFIG.md](BRAND_CONFIG.md) — Brand identity (colors, fonts, logo, signature elements, slide layouts)
- [html-template.md](html-template.md) — HTML architecture and JS features
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference

**Key requirements:**

- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use the exact fonts, colors, and CSS variables from BRAND_CONFIG.md. **Note:** Fontshare fonts have broken PostScript metadata that causes PDF export issues (see Phase 6B Font Safety). Google Fonts are recommended when PDF export is likely.
- Include the brand's logo on title and closing slides (and optionally as a small watermark on other slides, per the brand config's logo placement)
- Apply the brand's signature elements consistently across slides
- Follow the slide type layouts defined in the brand config
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Check brand config** — If BRAND_CONFIG.md doesn't exist, run Phase 2 first
4. **Generate HTML** — Convert to brand style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Clean up** — Delete `.claude-design/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save

---

## Phase 6: Share & Export (Optional)

After delivery, **ask the user:** _"Would you like to share this presentation? I can deploy it to a live URL (works on any device including phones) or export it as a PDF."_

Options:

- **Deploy to URL** — Shareable link that works on any device
- **Export to PDF** — Universal file for email, Slack, print
- **Both**
- **No thanks**

If the user declines, stop here. If they choose one or both, proceed below.

### 6A: Deploy to a Live URL (Vercel)

This deploys the presentation to Vercel — a free hosting platform. The link works on any device (phones, tablets, laptops) and stays live until the user takes it down.

**If the user has never deployed before, guide them step by step:**

1. **Check if Vercel CLI is installed** — Run `npx vercel --version`. If not found, install Node.js first (`brew install node` on macOS, or download from https://nodejs.org).

2. **Check if user is logged in** — Run `npx vercel whoami`.
   - If NOT logged in, explain: _"Vercel is a free hosting service. You need an account to deploy. Let me walk you through it:"_
     - Step 1: Ask user to go to https://vercel.com/signup in their browser
     - Step 2: They can sign up with GitHub, Google, email — whatever is easiest
     - Step 3: Once signed up, run `vercel login` and follow the prompts (it opens a browser window to authorize)
     - Step 4: Confirm login with `vercel whoami`
   - Wait for the user to confirm they're logged in before proceeding.

3. **Deploy** — Run the deploy script:

   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```

   The script accepts either a folder (with index.html) or a single HTML file.

4. **Share the URL** — Tell the user:
   - The live URL (from the script output)
   - That it works on any device — they can text it, Slack it, email it
   - To take it down later: visit https://vercel.com/dashboard and delete the project
   - The Vercel free tier is generous — they won't be charged

**Deployment gotchas:**

- **Local images/videos must travel with the HTML.** The deploy script auto-detects files referenced via `src="..."` in the HTML and bundles them. But if the presentation references files via CSS `background-image` or unusual paths, those may be missed. **Before deploying, verify:** open the deployed URL and check that all images load. If any are broken, the safest fix is to put the HTML and all its assets into a single folder and deploy the folder instead of a standalone HTML file.
- **Prefer folder deployments when the presentation has many assets.** If the presentation lives in a folder with images alongside it (e.g., `my-deck/index.html` + `my-deck/logo.png`), deploy the folder directly: `bash scripts/deploy.sh ./my-deck/`. This is more reliable than deploying a single HTML file because the entire folder contents are uploaded as-is.
- **Redeploying updates the same URL.** Running the deploy script again on the same presentation overwrites the previous deployment. The URL stays the same — no need to share a new link.

### 6B: Export to PDF

Two export methods are available. **Use the vector PDF method first** — it's faster, produces dramatically smaller files (~130KB vs ~20MB), preserves selectable text, and renders instantly in macOS Preview. Fall back to the screenshot method only if you encounter rendering issues with specific visual effects.

**Note:** Animations and interactivity are not preserved in either method — the PDF is a static snapshot. This is normal and expected; mention it to the user so they're not surprised.

#### Method 1: Vector PDF (recommended)

Uses Chromium's native PDF renderer with font patching. Produces small, fast, text-selectable PDFs.

```bash
npx -p playwright node scripts/export-pdf.js <path-to-html> [output.pdf]
```

**What happens behind the scenes:**
- Detects Fontshare fonts and patches their broken PostScript name tables (see Font Safety below)
- Rewrites the DOM to disable scroll-snap and force proper page breaks
- Strips transparent gradient overlays that cause sluggish rendering in Preview
- Generates a native vector PDF at standard widescreen dimensions (960×540 pts)
- Linearizes the PDF with qpdf for progressive page loading

**Prerequisites:**
- `npx playwright install chromium` — browser engine
- `pip3 install fonttools` — font patching (only needed if Fontshare fonts are detected)
- `brew install qpdf` — PDF linearization (optional but recommended)

**Typical result:** 17-slide deck = ~130KB, instant page flips in Preview, selectable text.

#### Method 2: Screenshot PDF (fallback)

Captures each slide as a PNG screenshot and combines them into a PDF. Use this if Method 1 has rendering issues with specific visual effects (e.g., canvas animations, complex SVGs).

```bash
bash scripts/export-pdf.sh <path-to-html> [output.pdf]
```

**Tradeoffs vs Method 1:**
- File size: ~1-2MB per slide (vs ~8KB per slide with Method 1)
- Text is NOT selectable (it's images)
- macOS Preview may be sluggish with large files
- Use `--compact` flag for smaller files: `bash scripts/export-pdf.sh <path> --compact`

#### Font Safety (IMPORTANT)

**Fontshare ships font files with broken metadata.** The PostScript name, family name, and full name fields in Fontshare's TTF files are literally set to the string `"false"`. This is not a Chromium bug — it's in the font binary itself. When Chromium embeds these fonts in a PDF, macOS Preview cannot cache or identify them, causing:
- Text blurs on every page flip, then re-renders after ~0.5 seconds
- Pages flash white when navigating
- Overall sluggish feel, as if the PDF has network dependencies

**The vector PDF script (Method 1) fixes this automatically** by downloading the TTF files, patching the name tables with Python fonttools, and injecting the corrected fonts as base64 during generation.

**If you're choosing fonts for a new presentation and PDF export is likely needed, prefer Google Fonts.** All Google Fonts have correct PostScript metadata and embed cleanly in PDFs without patching.

**⚠ Other PDF export gotchas:**

- **Slides must use `class="slide"`.** Both export scripts find slides by querying `.slide` elements.
- **Standard page dimensions matter.** The vector PDF script generates at 1280×720 CSS pixels → 960×540 PDF points. This is the exact standard widescreen format that macOS Preview, Keynote, and PowerPoint are optimized for. Larger dimensions (e.g., 1920×1080 → 1440×810 pts) cause Preview to re-render pages on every flip.
- **Transparent gradient overlays are expensive.** `::before` pseudo-elements with `hsla()` radial gradients create PDF transparency groups. The vector PDF script strips these automatically. The solid `--bg-primary` background looks clean without them.
- **Linearization helps.** `qpdf --linearize` reorganizes the PDF for progressive page loading. Without it, Preview may show white flashes between pages.

---

## Supporting Files

| File                                               | Purpose                                                         | When to Read                     |
| -------------------------------------------------- | --------------------------------------------------------------- | -------------------------------- |
| [BRAND_CONFIG.md](BRAND_CONFIG.md)                 | Brand identity: colors, fonts, logo, signature elements, layouts | Phase 0 (always) + Phase 3      |
| [viewport-base.css](viewport-base.css)             | Mandatory responsive CSS — copy into every presentation         | Phase 3 (generation)             |
| [html-template.md](html-template.md)               | HTML structure, JS features, code quality standards             | Phase 3 (generation)             |
| [animation-patterns.md](animation-patterns.md)     | CSS/JS animation snippets and effect-to-feeling guide           | Phase 3 (generation)             |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction                        | Phase 4 (conversion)             |
| [scripts/deploy.sh](scripts/deploy.sh)             | Deploy slides to Vercel for instant sharing                     | Phase 6 (sharing)                |
| [scripts/export-pdf.js](scripts/export-pdf.js)     | Vector PDF export with font patching (recommended)              | Phase 6 (PDF export)             |
| [scripts/export-pdf.sh](scripts/export-pdf.sh)     | Screenshot-based PDF export (fallback)                          | Phase 6 (PDF export)             |
