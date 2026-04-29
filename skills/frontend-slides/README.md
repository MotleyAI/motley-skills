# Branded Slides

A Claude Code skill for creating stunning, animation-rich HTML presentations — locked to your brand identity.

Fork of [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by [@zarazhangrui](https://github.com/zarazhangrui).

## What This Does

**Branded Slides** helps you create beautiful web presentations that always match your brand — without knowing CSS or JavaScript. On first use, a brand wizard walks you through defining your visual identity (colors, fonts, logo, signature elements). Every presentation after that is automatically on-brand.

### Key Features

- **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools, no frameworks.
- **Brand-Locked** — Every presentation uses your brand's visual identity. No style picker, no generic themes.
- **Brand Wizard** — Define your brand from a website, brand guidelines, an existing deck, or from scratch.
- **PPT Conversion** — Convert existing PowerPoint files to your branded web format.
- **Anti-AI-Slop** — Distinctive, custom-crafted design. No generic AI aesthetics.
- **Production Quality** — Accessible, responsive, well-commented code you can customize.

## How It Works

### First Time: Brand Wizard

The first time you use the skill, it runs a brand wizard that creates your `BRAND_CONFIG.md`:

1. **Choose your input** — the recommended path is to share an existing presentation (PPT/PPTX/HTML). Decks codify visual identity more completely than websites do.
   Other options: website URL (via dembrandt), brand guidelines PDF, or start from scratch.
2. **Review extracted identity** — colors, fonts, logo, overall feel
3. **Pick typography** — choose from proposed font pairings
4. **Define signature elements** — CSS-only visual patterns that make your slides distinctive
5. **Preview & approve** — see a sample title slide before committing

Your brand config is saved once and used for every future presentation.

#### Recommended: extract from an existing presentation

Most companies already have a deck template that codifies the brand more completely than a website (it includes pre-resolved decisions about logo placement, slide layouts, font weights for headings vs body, etc.). The wizard reads `.pptx` theme XML directly to pull the full color scheme, font scheme, and embedded logos at their highest resolution.

#### Extracting from a website (dembrandt)

If you don't have a deck template, the "From a website" path uses [**dembrandt**](https://github.com/dembrandt/dembrandt) — a tool that extracts any website's design system (colors, typography, logo, borders, components) into design tokens in seconds. The wizard runs it for you automatically; no install needed (it uses `npx`).

For richer integration, you can connect the dembrandt MCP server once and the skill will call its tools directly:

```bash
claude mcp add --transport stdio dembrandt -- npx -y dembrandt-mcp
```

### Every Time After: Create Presentations

```
/branded-slides

> "Create a pitch deck for our Series A"
```

The skill will:

1. Ask about your content (slides, messages, images)
2. Generate the full presentation in your brand's style
3. Open it in your browser
4. Optionally deploy to a live URL or export to PDF

### Convert a PowerPoint

```
/branded-slides

> "Convert quarterly-review.pptx to our brand"
```

Extracts all content from the PPT and rebuilds it in your brand's visual identity.

## Installation

### Via Plugin Marketplace

```bash
/plugin marketplace add yranchere/branded-slides
/plugin install branded-slides@branded-slides
```

Then use it by typing `/branded-slides` in Claude Code.

### Manual Installation

```bash
git clone https://github.com/yranchere/branded-slides.git ~/.claude/skills/branded-slides
```

Then use it by typing `/branded-slides` in Claude Code.

## Architecture

| File                      | Purpose                                          | Loaded When                      |
| ------------------------- | ------------------------------------------------ | -------------------------------- |
| `SKILL.md`                | Core workflow and rules                          | Always (skill invocation)        |
| `BRAND_CONFIG.md`         | Your brand identity (created by wizard)          | Always (Phase 0 check + Phase 3)|
| `viewport-base.css`       | Mandatory responsive CSS                         | Phase 3 (generation)             |
| `html-template.md`        | HTML structure and JS features                   | Phase 3 (generation)             |
| `animation-patterns.md`   | CSS/JS animation reference                       | Phase 3 (generation)             |
| `scripts/extract-pptx.py` | PPT content extraction                           | Phase 4 (conversion)             |
| `scripts/deploy.sh`       | Deploy to Vercel                                 | Phase 6 (sharing)                |
| `scripts/export-pdf.sh`   | Export slides to PDF                             | Phase 6 (sharing)                |

## Sharing Your Presentations

### Deploy to a Live URL

```bash
bash scripts/deploy.sh ./my-deck/
```

Uses [Vercel](https://vercel.com) (free tier). The skill walks you through signup and login if it's your first time.

### Export to PDF

```bash
bash scripts/export-pdf.sh ./presentation.html
```

Uses [Playwright](https://playwright.dev) to screenshot each slide at 1920x1080 and combine into a PDF.

## Updating Your Brand

To change your brand identity at any time, just ask:

> "Update my brand colors to use our new palette"

Or delete `BRAND_CONFIG.md` and the wizard will run again on the next invocation.

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- For PPT conversion: Python with `python-pptx` library
- For URL deployment: Node.js + Vercel account (free)
- For PDF export: Node.js (Playwright installs automatically)

## Credits

Based on [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by [@zarazhangrui](https://github.com/zarazhangrui).

## License

MIT — Use it, modify it, share it.
