---
name: make-slides
description: Create branded HTML presentations using structured slide specs. Outputs JSON DeckSpec instead of raw HTML — the server handles all rendering, styling, and viewport fitting.
---

# Make Slides

Create branded HTML/PDF presentations by describing slide content declaratively.
You specify **what** goes on each slide (layouts, text, data, charts); the server
handles **how** it renders (HTML, CSS, animations, logos, waves, charts, tables).

## When to trigger

Activate when the user asks to create slides, a deck, a presentation, or a report
in any of these forms: "make me slides", "create a presentation", "build a deck",
"slide deck", "PowerPoint", "PDF slides".

---

## Phase 1: Content Discovery

Ask the user these questions (skip any already answered):

1. **Purpose** — What is this presentation about? Who is the audience?
2. **Length** — Roughly how many slides? (Suggest 5-8 for a focused deck, 10-15 for detailed.)
3. **Content** — Do you have content ready (data, text, bullet points), or should I draft it?
4. **Data** — Are there charts or tables from a Motley document to include? (If yes, get the document ID and block names.)

---

## Phase 2: Load Layouts

1. Call **`list_resources(what="styles")`** to see available brand styles.
2. Ask the user which style to use (or pick the default if only one exists).
3. Call **`read_layouts(style_name="chosen_style")`** to get the layout catalog.

> **IMPORTANT:** Layout names, panel counts, and constraints differ across styles.
> Each style has its own set of layouts — they are **not** interchangeable.
> You **MUST** call `read_layouts` for the specific style you are building for —
> never reuse layout names from another style or from the example at the bottom
> of this file. Using a wrong layout name will cause `save_deck` to fail.

The catalog returns a list of layouts, each with:
- **name** — Layout identifier (use these **exactly** as returned — they are style-specific)
- **when_to_use** — Guidance on when this layout fits
- **panels** — List of panel slots, each describing:
  - Which header fields are supported (badge, title, subtitle, aside)
  - Which body content types are allowed (prose, data_points, cards, tags, chart, table)
  - Notes with constraints (e.g. "Exactly 3 data points")

---

## Phase 3: Build DeckSpec

Construct a JSON **DeckSpec** object. The schema:

```json
{
  "slides": [
    {
      "layout": "Layout Name",
      "panels": [
        {
          "badge": "",
          "title": "Heading text",
          "subtitle": "Text below heading",
          "aside": "Right-aligned note",
          "body": { "kind": "...", ... }
        }
      ]
    }
  ]
}
```

### Content block types (the `body` field)

| kind | Fields | Use for |
|------|--------|---------|
| `prose` | `text` (markdown) | Paragraphs, bullet lists, inline formatting |
| `data_points` | `columns` (int, 0=auto), `items` (list of `{value, label, detail?, highlighted?}`) | Metrics, KPIs, funnel stages, summary rows |
| `cards` | `columns` (int, 0=auto), `items` (list of `{title, body}`) | Multi-column content, recommendation cards |
| `tags` | `items` (list of `{text, highlighted?}`) | Tag/pill clouds, company lists |
| `chart` | `block_name` (string) | Reference to a chart block in a Motley document |
| `table` | `block_name` (string) | Reference to a table block in a Motley document |

### Panel header fields

All header fields accept **either** a raw string **or** a block reference from the
source Motley document. Block references are resolved server-side before rendering.

| Field | Purpose | Example |
|-------|---------|---------|
| `badge` | Small label above title (eyebrow, section tag) | `"Section 01"` or `{"kind": "text_block_ref", "block_name": "section_label"}` |
| `title` | Main heading (supports `\n` for line breaks) | `"Q1 Results"` or `{"kind": "text_block_ref", "block_name": "report_title"}` |
| `subtitle` | Text below title (supports markdown) | `"**Jan–Mar 2025**"` or `{"kind": "query_block_ref", "block_name": "date_range"}` |
| `aside` | Right-aligned secondary text | `"Jan – Dec 2025"` or `{"kind": "query_block_ref", "block_name": "period"}` |

**Block reference types:**
- `{"kind": "text_block_ref", "block_name": "..."}` — resolves to the text block's markdown content, rendered as HTML.
- `{"kind": "query_block_ref", "block_name": "..."}` — resolves to the query block's formatted value (e.g. "$1.2M"). Only single-number mode queries are supported.

The `prose` body type's `text` field also accepts these block references.

### Rules

- **First slide**: Always use the first layout (typically "Title" or "Cover").
- **Last slide**: Always use the closing layout.
- **Split layouts**: Provide exactly 2 panels (left, right).
- **Single-panel layouts**: Provide exactly 1 panel.
- **Content density**: Follow the `notes` in each panel slot — don't overfill.
- **Chart/table refs**: Use exact block names from the Motley document.
- **No literal numbers**: Text elements must NEVER contain a single literal number (e.g. `"$1.2M"`, `"340%"`, `"1,234"`). This applies to header fields, prose text, **and** `data_points` `value`/`detail` fields. Instead, always use a `query_block_ref` or `text_block_ref` pointing to the block that produced that number. This ensures values stay in sync with the underlying data.

---

## Phase 4: Deliver

1. Call **`save_deck(deck_spec=<your JSON>, style_name="chosen_style", title="Presentation Title", source_document_id=<if charts/tables>)`**
   - This copies referenced blocks from the source document, resolves them, and persists the deck.
   - Returns `{"document_id": <new_id>}`.
2. Call **`export_document(document_id=<new_id>, format="html")`** to render the HTML.
3. Present the `html_url` to the user.
4. If the user wants PDF, call **`export_document(document_id=<new_id>, format="pdf")`**.

---

## Example: Cledara 4-slide deck

```json
{
  "slides": [
    {
      "layout": "Title",
      "panels": [{"title": "Q1 2025 SaaS Report", "subtitle": "Prepared for the Board"}]
    },
    {
      "layout": "Content + Badge",
      "panels": [{
        "badge": "Overview",
        "title": "Key Findings",
        "body": {"kind": "prose", "text": {"kind": "text_block_ref", "block_name": "key_findings"}}
      }]
    },
    {
      "layout": "Three-Column Metrics",
      "panels": [{
        "title": "Key Metrics",
        "body": {"kind": "data_points", "columns": 3, "items": [
          {"value": {"kind": "query_block_ref", "block_name": "arr_total"}, "label": "ARR"},
          {"value": {"kind": "query_block_ref", "block_name": "growth_rate"}, "label": "Growth"},
          {"value": {"kind": "query_block_ref", "block_name": "retention_rate"}, "label": "Retention"}
        ]}
      }]
    },
    {
      "layout": "Closing / Thank You",
      "panels": [{"title": "Thank You", "subtitle": "Questions? team@example.com"}]
    }
  ]
}
```
