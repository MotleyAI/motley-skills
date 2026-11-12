# Motley

Query your business data through a semantic layer, and build dashboards, reports, and automations from live data.

Motley gives Claude a shared set of metric definitions, dimensions, and table relationships for your connected database. Claude asks questions with those definitions instead of writing one-off SQL, so answers stay consistent and you can see how each number was calculated. Business context you save once is reused in every later analysis.

## What you can do

- **Ask questions about your data.** KPIs, trends, comparisons, rankings, and breakdowns, computed from your governed definitions.
- **Build dashboards and reports.** Documents with text, tables, and charts that run on live data and stay up to date.
- **Power Claude's automations.** Recurring workflows that Claude runs, such as a weekly KPI summary, use Motley as their live data backend.
- **Set up and curate the semantic layer.** Describe tables, define metrics such as revenue or active customers, and verify them against real questions.
- **Save business context** so future analyses use the same definitions.

## Try asking

- "What data do I have in Motley?"
- "What was revenue by store last quarter?"
- "Which five products had the highest sales this year?"
- "Create a report on store performance with a summary, a table of orders by store, and a monthly trend chart."
- "Remember that 'active customer' means a customer with at least one order in the last 90 days."

## Skills

| Skill | What it does |
|-------|--------------|
| `get-started` | Check which data is available, see what you can ask, and set up the semantic layer if needed. |
| `create-report` | Create a document with text, tables, and charts from your data. |
| `semantic-layer-bootstrap` | Set up, curate, and verify the semantic layer for your data source. |

New to Motley? Start with `get-started`. On a fresh data source, run `semantic-layer-bootstrap` first.

## Requirements

A [Motley](https://motley.ai) account. You can connect your own database or try Motley with demo data. Editing semantic definitions requires the editor role.

## Data and privacy

The plugin contains only skills (Markdown instructions) and the configuration for one remote MCP server, `https://app.motley.ai/api/v1/mcp`. It runs no local code and has no hooks. All tool calls go to that server and are authenticated with OAuth against your Motley account. Motley reads only the data sources your organization connects. It does not change data in your databases.

- [Documentation](https://docs.motley.ai/motley/)
- [Privacy policy](https://motley.ai/legal/privacy-policy)
- [Terms of service](https://motley.ai/legal/terms-of-service)
- [Support](https://motley.ai/support)

## Install

Install Motley from this repository, or connect the server URL `https://app.motley.ai/api/v1/mcp` directly, to get every Motley feature. This includes agent feedback prompts, which editors turn on in **Settings → MCP** in the Motley app. Motley listings in the Claude and ChatGPT directories never send feedback prompts.

### Claude Code

```
/plugin marketplace add MotleyAI/motley-skills
/plugin install motley@motley-plugins
```

Then run `/mcp`, select **motley**, and sign in.

### Claude Cowork

1. Open **Customize → Personal plugins**.
2. Add the marketplace `MotleyAI/motley-skills`. Enable auto updates.
3. Install the **Motley** plugin.
4. Authenticate the Motley connector in the browser.

### Claude on the web and desktop

1. Open **Settings → Connectors** and choose **Add custom connector**.
2. Enter the name `Motley` and the URL `https://app.motley.ai/api/v1/mcp`.
3. Choose **Connect** and sign in to Motley.

On Team and Enterprise plans, an owner adds the connector once for the whole organization in **Organization settings → Connectors**. Members then choose **Connect**.

A connector adds the Motley tools only. To also get the skills, install the plugin in Claude Code or Cowork.

### ChatGPT

Add a custom connector with the URL `https://app.motley.ai/api/v1/mcp` and sign in to Motley. Custom connectors need developer mode. See [OpenAI's guide](https://help.openai.com/en/articles/11487775-connectors-in-chatgpt) for the steps on your plan.

### Codex, Cursor, and other agents

Install the skills with [skills.sh](https://skills.sh):

```
npx skills add MotleyAI/motley-skills
```

Then connect the Motley MCP server. The endpoint is `https://app.motley.ai/api/v1/mcp` (HTTP with OAuth).

**Codex** — add to `~/.codex/config.toml`:

```toml
[mcp_servers.motley]
url = "https://app.motley.ai/api/v1/mcp"
```

**Cursor** — add to `~/.cursor/mcp.json`:

```json
{ "mcpServers": { "motley": { "url": "https://app.motley.ai/api/v1/mcp" } } }
```

## About

Motley is built on [SLayer](https://github.com/MotleyAI/slayer), its open-source semantic engine.
