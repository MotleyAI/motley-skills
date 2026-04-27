---
name: update-chart
description: >
  Create or modify charts using update_chart_block. Covers chart type selection,
  structured query and chart_details parameters, and verification with render_chart.
---

# Update Chart

Create or modify chart blocks using the `update_chart_block` MCP tool. You provide a structured query and chart configuration directly — no LLM intermediary.

## How It Works

1. Call `update_chart_block` with a `query` (what data to fetch) and `chart_details` (how to render it)
2. The query is validated and the chart configuration is saved to the block
3. Call `render_chart` to see the rendered PNG (this also triggers resolution)

## Tool Signature

```
update_chart_block(
    location: {                # Location of the chart block
        doc_id: int,           # The document ID
        slide_name: str,       # The slide containing the chart block
        block_name: str        # The name of the chart block
    },
    query: {                   # Semantic layer query (MinimalSemanticLayerQueryForLLM)
        measures: [            # List of measures to aggregate
            {name: str, cube_name: str?}
        ],
        dimensions: [          # List of dimensions to group by
            {name: str, cube_name: str?}
        ]?,
        time_dimension: {      # Single time dimension (NOT a list)
            dimension: {name: str, cube_name: str?},
            granularity: str?  # "day", "week", "month", "quarter", "year"
        }?,
        filters: [...]?,       # Filters array
        limit: int?,           # Max rows to return
        order: [               # Ordering
            {column: {name: str, cube_name: str?}, order: "ASC"|"DESC"}
        ]?
    },
    chart_details: {           # Chart rendering configuration (ChartDetailsTemplate)
        series: {...},         # Series configs by name
        x_axis: {lines: bool, label: str?, scale: ("LINEAR"|"LOG")?},
        y_axis: {lines: bool, label: str?, scale: ("LINEAR"|"LOG")?},
        y_right_axis: {...}?,  # Right Y axis (for dual axis)
        series_default: {type: "BAR"|"LINE"|"PIE"|"FUNNEL", y_axis: "left"|"right", ...},
        color_scheme: str?,    # e.g. "motley", "greens", "blues"
        title: str?,
        legend: {enabled: bool, location: str, orientation: "VERTICAL"|"HORIZONTAL"}?
    },
    sample_values: {str: str}?,   # Override filter values (e.g. start_date, end_date)
    max_return_rows: int? = 20,   # Max rows in response preview
    add_default_filters: bool? = true  # Apply default time/tenant filters
)
```

**Returns**: Confirmation that the chart was updated with a data preview. Does NOT return a rendered image — use `render_chart` for that.

The full nested schemas for `query` and `chart_details` come from the tool definition. The above shows the most commonly used fields.

In the `query` schema, `cube_name` is the model name — the API still uses the historical `cube_name` label for this field. Pass the same name you'd give to `inspect_model`.

When `add_default_filters=true` (the default), the model's default time dimension is filtered between the document's `start_date` and `end_date` automatically — you don't need to add a time filter to your `query` spec. Set it to `false` only for charts that should ignore the document's date range.

## Chart Type Guidance

| Type | Best For | Example |
|------|----------|---------|
| **BAR** | Categorical comparisons, rankings, time series with few points | Revenue by region |
| **LINE** | Trends over time, continuous data, multiple series comparison | Monthly active users over 12 months |
| **PIE** | Part-to-whole relationships, distribution (use sparingly, max 5-7 segments) | Revenue distribution by category |
| **FUNNEL** | Conversion stages, sequential process drop-off | Sales funnel from lead to close |

### Tips

- **Bar vs Line**: Use bars for categorical comparisons or few time points. Use lines for trends with many time points.
- **Pie charts**: Only effective with 5-7 or fewer segments. For more categories, use a bar chart.
- **Dual axis**: Useful when comparing measures with different scales (e.g., revenue in dollars vs count of orders). Set `y_axis: "right"` on the secondary series.
- **Stacked bars**: Use the same `x_axis` dimension with multiple measures, all as BAR type.
- **Horizontal bars**: Use BAR type with dimensions on the y-axis — good for long category labels or ranking displays.

## Examples

### Time Series — Monthly Revenue

```
update_chart_block(
    location={doc_id: 42, slide_name: "Revenue Trends", block_name: "revenue_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "revenue"}],
        time_dimension: {
            dimension: {name: "created_at", cube_name: "revenue"},
            granularity: "month"
        },
        limit: 12,
        order: [{column: {name: "created_at", cube_name: "revenue"}, order: "ASC"}]
    },
    chart_details={
        series_default: {type: "LINE", y_axis: "left", number_format: {style: "currency"}, show_values: false},
        x_axis: {lines: false, label: false},
        y_axis: {lines: true, label: "Revenue"},
        y_right_axis: {lines: false},
        title: "Monthly Revenue"
    }
)
```

### Categorical — Top Regions

```
update_chart_block(
    location={doc_id: 42, slide_name: "Regional Performance", block_name: "region_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "sales"}],
        dimensions: [{name: "region", cube_name: "sales"}],
        limit: 10,
        order: [{column: {name: "total_revenue", cube_name: "sales"}, order: "DESC"}]
    },
    chart_details={
        series_default: {type: "BAR", y_axis: "left", number_format: {style: "currency"}, show_values: true},
        x_axis: {lines: false, label: "Region"},
        y_axis: {lines: true, label: "Revenue"},
        y_right_axis: {lines: false},
        title: "Top 10 Regions by Revenue"
    }
)
```

### Dual Axis — Revenue vs Count

```
update_chart_block(
    location={doc_id: 42, slide_name: "Overview", block_name: "dual_chart"},
    query={
        measures: [
            {name: "total_revenue", cube_name: "orders"},
            {name: "order_count", cube_name: "orders"}
        ],
        time_dimension: {
            dimension: {name: "created_at", cube_name: "orders"},
            granularity: "month"
        },
        limit: 12
    },
    chart_details={
        series: {
            "total_revenue": {type: "BAR", y_axis: "left", number_format: {style: "currency"}, show_values: false},
            "order_count": {type: "LINE", y_axis: "right", number_format: {style: "decimal"}, show_values: false}
        },
        series_default: {type: "BAR", y_axis: "left"},
        x_axis: {lines: false, label: false},
        y_axis: {lines: true, label: "Revenue"},
        y_right_axis: {lines: true, label: "Orders"},
        title: "Revenue vs Order Count"
    }
)
```

### Pie — Distribution

```
update_chart_block(
    location={doc_id: 42, slide_name: "Breakdown", block_name: "pie_chart"},
    query={
        measures: [{name: "total_revenue", cube_name: "products"}],
        dimensions: [{name: "category", cube_name: "products"}],
        limit: 5,
        order: [{column: {name: "total_revenue", cube_name: "products"}, order: "DESC"}]
    },
    chart_details={
        series_default: {type: "PIE", y_axis: "left", number_format: {style: "currency"}, show_values: true},
        x_axis: {lines: false},
        y_axis: {lines: false},
        y_right_axis: {lines: false},
        title: "Revenue by Category",
        legend: {enabled: true, location: "auto", orientation: "VERTICAL"}
    }
)
```

## Resolution Behavior

Charts are **NOT resolved immediately** after `update_chart_block`. The chart config is saved, but no data is fetched or rendered yet.

To see the chart:
- **Individual chart**: Call `render_chart(location={doc_id: ..., slide_name: ..., block_name: ...})` — this triggers resolution and returns a PNG image

## Verifying Charts

**Always call `render_chart` after `update_chart_block`** to visually verify the result.

```
render_chart(
    location={doc_id: 42, slide_name: "Revenue Trends", block_name: "revenue_chart"},
    width=800,
    height=600
)
```

Check the returned image for:
- Correct chart type
- Appropriate axis labels and scales
- Data looks reasonable (no obviously wrong values)
- Legend is readable
- Time series is in chronological order

If the chart doesn't look right, call `update_chart_block` again with adjusted `query` or `chart_details`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Wrong chart type | Set `series_default.type` explicitly (BAR, LINE, PIE, FUNNEL) |
| Missing data points | Check that the model has data for the requested time range. Use `inspect_model` to verify. |
| Too many categories | Add `limit` to the query |
| Wrong time granularity | Set `time_dimension.granularity` explicitly |
| Axis scale issues | Set `scale: "LOG"` on the axis, or use dual axis with `y_axis: "right"` |
| Unknown measure/dimension | Use `inspect_model` to see exact names |
| Wrong model | Set `cube_name` (i.e. the model name) on each measure/dimension explicitly |

## Related Skills

- For exploring models before building charts: see the `explore-model` skill
- For understanding model schemas: see [model-guide.md](../../shared/model-guide.md)
