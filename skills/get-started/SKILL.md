---
name: get-started
description: Get a new user started with Motley. Check which data is available, show what the user can ask, and set up the semantic layer if it is missing. Use when the user is new to Motley, asks what Motley can do, or asks what data they have.
---

# Get started with Motley

Find out what data the user has. Then help the user take the next step. Adapt to the user's situation. Keep your messages short and simple.

## 1. Check the data

Use `list_resources(what="datasources")` to see the connected data sources.

## 2. Demo data only

If the only source is the demo database (Jaffle Shop, a fictional café chain), tell the user. Give a few example questions, for example:

- What is the total revenue by store?
- How did monthly revenue grow this year?
- What are the best-selling items?

Offer to answer one of them.

## 3. The user's own data

Use `search` to read some memories, and `inspect` a few models. Decide if the semantic layer is set up: the models have descriptions, measures, and joins.

- **Set up:** say in a few words what data is available. Ask what the user wants to do: ask a question, give context to improve the semantic layer, or set up an automation.
- **Not set up, or empty:** use the `semantic-layer-bootstrap` skill to set it up.

To connect a new data source, the user contacts the Motley team at support@motley.ai.
