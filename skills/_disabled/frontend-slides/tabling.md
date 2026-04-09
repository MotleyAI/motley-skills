# Table Integration Guide

## Rule: NEVER Generate Table Data or Markup Yourself

**All tables come from Motley MCP tools.** Never generate table data, `<table>` markup, or table styling yourself.

## Getting a Table

- If the Storyline document already has a table block -> it's already resolved
- If no table exists -> call `update_table_block` with a prompt describing the desired table, specifying a location in the document

## Embedding Tables in Body HTML

**Do NOT generate any `<table>` HTML.** The server handles all table rendering and styling.

Place a table container with a `data-table-block` attribute referencing the table block by name:

```html
<div id="table-1" class="table-container rv" data-table-block="quarterly_metrics"></div>
```

The server searches all slides in the source document for a block with this name, converts its data to a styled `<table>` element using the brand's `table_css_class`, and injects it into the container.

### Example

If the source document has a table block named `quarterly_metrics`:

```html
<section class="slide slide-data" id="slide-4">
  <div class="topbar">
    <div class="logo on-light rv"><!-- logo --></div>
    <span class="pg-num rv">04 / 07</span>
  </div>
  <div class="s-hdr rv">
    <span class="accent-bar"></span>
    <span class="s-title">Quarterly Metrics</span>
  </div>
  <div class="content-body">
    <div id="table-1" class="table-container rv" data-table-block="quarterly_metrics"></div>
  </div>
</section>
```

### Requirements

- **Every** `table-container` element **must** have a `data-table-block` attribute. Missing refs cause an error.
- The referenced table block must be resolved (call `update_table_block` first if needed).
- Each table container must have a unique `id` attribute.
- The server generates the `<table>` HTML with the brand's CSS class applied automatically.

## What You Do NOT Generate

- No `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` tags
- No table data or cell values
- No inline table styling

All of this is handled server-side during HTML enrichment.
