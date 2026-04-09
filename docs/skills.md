# Skills Reference

This document provides an overview of the skills included in the Motley bundle. Skills help Claude understand how to work with the Motley MCP tools for data-driven report generation.

## When to Use Each Skill

| Task | Skill |
|------|-------|
| Create a report end-to-end | [create-report](#create-report) |
| Create or modify a chart | [update-chart](#update-chart) |
| Create or modify text content | [update-text-block](#update-text-block) |
| Create or modify a table | [update-table-block](#update-table-block) |
| Create data queries for text/tables | [update-query-block](#update-query-block) |
| Explore available data | [explore-cube](#explore-cube) |

---

## Core Skills

### create-report

End-to-end workflow for creating a data-driven report in Motley.

**When to use**: Creating a report, building a document, or making a data-driven presentation from scratch.

**Phases:**
1. Research & Plan — explore cubes, understand user needs
2. Create Document — initialize document, set context variables, create blocks via block-modifier sub-agent
3. User Approval — export markdown, present for feedback
4. Output — generate slides via make-slides skill

[Full documentation](../skills/create-report/SKILL.md)

---

### update-chart

Create or modify charts using `update_chart_block` with structured query and chart configuration.

**When to use**: Creating any chart or graph visualization (bar, line, pie, funnel).

**Key concepts:**
- Structured input: provide `query` (data) and `chart_details` (rendering) directly
- Chart types: BAR, LINE, PIE, FUNNEL
- Charts resolve lazily — call `render_chart` to see results
- Dual axis, stacked bars, period comparisons all supported via configuration

**Chart types:**

| Type | Best For |
|------|----------|
| BAR | Categorical comparisons, time series |
| LINE | Trends over time, continuous data |
| PIE | Part-to-whole, distribution |
| FUNNEL | Conversion stages, sequential processes |

[Full documentation](../skills/update-chart/SKILL.md)

---

### update-text-block

Create or modify text blocks using `update_text_block` with template syntax.

**When to use**: Creating text content that includes data values, summaries, or LLM-generated insights.

**Key concepts:**
- Template syntax with `{variable}` placeholders and formatting functions
- Three modes: direct substitution, LLM generation, constrained output
- Resolves immediately — result returned inline
- Cross-slide references via `{Slide::Block}`

**Mode selection:**

| Mode | Use Case |
|------|----------|
| `call_llm=false` | Fixed template with data substitution |
| `call_llm=true` | LLM-generated content from data |
| `call_llm=true` + `allowed_outputs` | Constrained categorization |

[Full documentation](../skills/update-text-block/SKILL.md)

---

### update-table-block

Create or modify table blocks using `update_table_block` with size constraints.

**When to use**: Creating data tables, comparison tables, or any tabular content.

**Key concepts:**
- `target_shape` for size constraints: `[rows, cols]` with exact, range, or null values
- Three patterns: raw query output, markdown template, LLM-generated
- Resolves immediately — result returned inline

**target_shape formats:**

| Format | Description |
|--------|-------------|
| `null` | No constraint |
| `[5, 3]` | Exactly 5 rows, 3 columns |
| `[[1, 10], null]` | 1-10 rows, any columns |

[Full documentation](../skills/update-table-block/SKILL.md)

---

### update-query-block

Create or modify numerical queries within text or table blocks.

**When to use**: When text or table blocks need data values. Queries are created first, then referenced as `{query_name}` in templates.

**Key concepts:**
- `single_number` mode for KPIs and inline values
- `table` mode for multi-row data and cross-tabs
- `pivot_dimension` and `transpose` for flexible table layouts
- Structured `query` parameter with measures, dimensions, filters
- Must create queries BEFORE referencing in text/table templates

[Full documentation](../skills/update-query-block/SKILL.md)

---

### explore-cube

Explore available cubes to understand what data is available.

**When to use**: Before building a report — discover cubes, inspect schemas, create custom cubes/measures.

**Key tools:**
- `cubes_summary()` — list all cubes
- `inspect_cube(cube_name=..., num_rows=3)` — see schema and sample data
- `create_cube(...)` — create custom cube from SQL
- `add_measures(...)` / `add_dimensions(...)` — extend existing cubes

[Full documentation](../skills/explore-cube/SKILL.md)

---

## Shared Reference Documents

These documents provide foundational knowledge used across skills:

### variable-reference-syntax.md

Expression syntax for templates:
- Variable references `{name}`
- Arithmetic operations
- Formatting functions (percent, integer, number, currency)
- Cross-slide references `{Slide::Block}`

[View](../skills/_shared/variable-reference-syntax.md)

### resolution-context.md

Auto-generated context variables:
- end_month, start_month, quarter
- now_date, now_month
- customer_name alias
- Using variables in filters and templates

[View](../skills/_shared/resolution-context.md)

### cube-guide.md

Cube data modeling concepts:
- Measures and dimensions
- Time granularities
- Dimension constraints for charts
- Filter concepts
- Custom cubes and measures

[View](../skills/_shared/cube-guide.md)

---

## Quick Reference

### Expression Functions

| Function | Description | Example |
|----------|-------------|---------|
| `{percent(x)}` | Format as percentage | `{percent(0.45)}` -> "45%" |
| `{integer(x)}` | Round to integer | `{integer(3.7)}` -> "4" |
| `{number(x, decimals=N)}` | Format with decimals | `{number(3.14159, decimals=2)}` -> "3.14" |
| `{currency(x)}` | Format as currency | `{currency(1000)}` -> "$1,000" |
| `{sum(ref)}` | Sum numeric columns | `{sum(Chart)}` |

### Time Granularities

| Granularity | Use Case |
|-------------|----------|
| `DAY` | Daily data |
| `WEEK` | Weekly rollups |
| `MONTH` | Monthly reports |
| `QUARTER` | Quarterly analysis |
| `YEAR` | Annual comparisons |

### Chart Types

| Type | Best For |
|------|----------|
| BAR | Categorical comparisons |
| LINE | Trends over time |
| PIE | Part-to-whole |
| FUNNEL | Conversion stages |

---

## Related Documentation

- [MCP Tools Reference](tools.md) - All MCP tools
- [Setup Guide](setup.md) - Installation and configuration
