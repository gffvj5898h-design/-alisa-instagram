# Product mailbox: ChatGPT ↔ GitHub ↔ Grok

This is the no-model-API operating mode for coordination v3.

## Principle

The products do the reasoning. GitHub does transport, validation and canonical state mutation.

Neither ChatGPT nor Grok directly edits `coordination/state.json` or creates canonical `coordination/messages/` files in v3.

Each product agent only:

1. reads current `coordination/state.json`;
2. acts only when `next_actor` equals that product;
3. reads `message_path` and relevant project files;
4. performs its work using its normal product tools/connectors;
5. creates one new proposal JSON under `coordination/proposals/`;
6. stops and lets GitHub Actions broker validate/apply the turn.

## ChatGPT product

Use a ChatGPT condition-watch against the repository. The watch must be silent when `next_actor != chatgpt`.

When `next_actor == chatgpt`:

- read `PROJECT_INSTRUCTIONS.md`, `coordination/PROTOCOL_V3.md`, state and `message_path`;
- hash/read the exact current state before composing the proposal;
- perform the required task;
- create one proposal JSON matching `coordination/agent_response.schema.json`;
- never write canonical state/message files directly;
- do not notify the user merely to relay the handoff.

Current platform constraint: the product-side periodic checker cannot run more often than hourly in this environment.

## Grok product

Use the authenticated GitHub connector and a Grok Bot routine when available.

Preferred trigger: a narrow supported GitHub event/notification associated with the coordination repository. If that trigger is not available for the account, use a periodic routine.

When `next_actor == grok`, follow the same proposal-only rule as ChatGPT.

Do not use a broad listener that reacts to every repository event; narrow it to the coordination repository/task to reduce noise and usage.

## GitHub Actions broker

`ai-proposal-apply-v3.yml` is the canonical single writer.

A valid proposal is tied to the exact current state SHA. Proposal apply runs are serialized. If two agents/proposals race from the same old state, the later stale proposal is rejected.

Modes:

- `dry_run`: validate and show the plan only;
- `product_mailbox`: apply the proposal, create canonical message/state and commit as GitHub Actions bot.

## Cost model

This design does not require `OPENAI_API_KEY` and does not invoke the OpenAI API.

Normal product/subscription limits still apply to ChatGPT and Grok. Any optional provider-specific add-on/on-demand usage is outside this protocol and must not be enabled implicitly.

## Activation gate

Do not switch `main` to v3 until all of the following are proven on the prototype branch:

1. product agent can create a conforming proposal;
2. proposal workflow validates it in `dry_run`;
3. broker applies one disposable proposal in `product_mailbox`;
4. stale/race proposal is rejected;
5. ChatGPT periodic checker uses proposal-only writes;
6. Grok routine uses proposal-only writes;
7. no user relay is required.
