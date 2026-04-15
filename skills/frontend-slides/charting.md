# Chart Integration Guide

## Rule: NEVER Generate Chart Data or Code Yourself

**All charts come from Motley MCP tools.** Never generate chart data, chart series configurations, or eCharts option code yourself.

## Getting a Chart

- If the Storyline document already has a chart block -> call `render_chart` to resolve it (returns a PNG image and `chart_config`)
- If no chart exists -> call `update_chart_block` with a prompt describing the desired chart, specifying a location in the document. This returns a confirmation with data preview, a PNG image, and the `chart_config` needed for embedding.

## Embedding Charts in Body HTML

**Do NOT embed any chart initialization JavaScript.** The server handles all chart rendering.

Place a chart container with a `data-chart-block` attribute referencing the chart block by name:

```html
<div id="chart-1" class="chart-container rv" data-chart-block="monthly_spend_trend"></div>
```

The server searches all slides in the source document for a block with this name.

### Example

If the source document has a chart block named `monthly_spend_trend`:

```html
<section class="slide slide-data" id="slide-3">
  <div class="topbar">
    <div class="logo on-light rv"><!-- logo --></div>
    <span class="pg-num rv">03 / 07</span>
  </div>
  <div class="s-hdr rv">
    <span class="accent-bar"></span>
    <span class="s-title">Monthly Spend Trend</span>
  </div>
  <div class="content-body">
    <div id="chart-1" class="chart-container rv" data-chart-block="monthly_spend_trend"></div>
  </div>
</section>
```

### Requirements

- **Every** `chart-container` element **must** have a `data-chart-block` attribute. Missing refs cause an error.
- The referenced chart block must be resolved (call `render_chart` first if needed).
- Each chart container must have a unique `id` attribute.
- The server fetches chart configs from the source document, applies brand colors, and generates all initialization JS.

## What You Do NOT Generate

- No `<script src="...echarts...">` CDN tags
- No `echarts_config.min.js` inlining
- No `echarts.init()` calls
- No `chartConfigToEChartsOption()` calls
- No `chart_config` JSON embedding

All of this is handled server-side during HTML enrichment.
