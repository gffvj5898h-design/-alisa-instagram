# Agent proposal inbox

This directory is the only coordination write surface used directly by the ChatGPT and Grok product agents in protocol v3.

Each agent turn creates exactly one new JSON proposal file here. The agent MUST NOT edit `coordination/state.json` or create the canonical handoff message itself.

Suggested filename:

`YYYYMMDD-HHMMSS-<actor>-turn-<turn_id>-<short-slug>.json`

Requirements:

- conform to `coordination/agent_response.schema.json`;
- `actor` must equal current `state.next_actor`;
- `expected_parent_state_sha` must equal the exact state blob SHA the agent consumed;
- `turn_id` must equal current `state.turn_id + 1`;
- one proposal per commit;
- old proposal files are immutable audit records;
- never put credentials, cookies, bearer tokens or private download URLs in a proposal.

A GitHub Actions broker validates a new proposal against the current state. Valid proposals may be applied by the broker; stale or unauthorized proposals fail without changing canonical state.
