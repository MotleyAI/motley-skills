# Chart Integration Guide

## Rule: NEVER Generate Chart Data or Code Yourself

**All charts come from Motley MCP tools.** Never generate chart data, chart series configurations, or eCharts option code yourself.

## Getting a Chart

- If the Storyline document already has a chart block → call `render_chart` to get its `chart_config`
- If no chart exists → call `update_chart_block` with a prompt describing the desired chart, specifying a location in the document. Use the returned `chart_config`.

## Getting Brand Colors for Charts

1. Call `read_style` to get the BrandConfig
2. If `default_chart_color_scheme` is set, pass it as the second arg to `chartConfigToEChartsOption`
3. If not set but `colors.tokens` exist, extract the hex values and pass as an array:
   `chartConfigToEChartsOption(config, ["#016FFF", "#FF6B35", ...])`
4. If neither, omit the second arg (uses the chart's embedded color scheme)

## Embedding an Interactive eChart in HTML

Load eCharts from CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script>
```

Read and inline the contents of `echarts_config.min.js` in a `<script>` tag.

Create a container:
```html
<div id="chart-N" style="width: 100%; height: min(60vh, 500px);"></div>
```

Initialize:
```javascript
const chartConfig = <chart_config JSON>;
const colorOverride = <from read_style, or null>;
const option = window.chartConfigToEChartsOption(chartConfig, colorOverride);
const chart = echarts.init(document.getElementById('chart-N'));
chart.setOption(option);
window.addEventListener('resize', () => chart.resize());
```

## Available Named Color Schemes

`"motley"`, `"greens"`, `"blues"`, `"light"`, `"chromatica"`, `"flash"`

## Fallback

If MCP tools are unavailable, embed a static PNG via `<img src="data:image/png;base64,...">`

## Sizing

Chart containers respect viewport fitting — `height: min(60vh, 500px)`. Always call `chart.resize()` on window resize.
