# Coordination v4 migration review checklist

Production activation is allowed only after all items below pass.

## Control plane

- [ ] `coordination/validate_state.py` passes.
- [ ] `coordination/test_v4_guards.py` passes.
- [ ] stale proposal is rejected.
- [ ] wrong actor is rejected.
- [ ] protected control-plane / executable path mutation is rejected.
- [ ] mailbox piggyback commit is rejected.
- [ ] broker creates exactly one canonical transition commit.
- [ ] `turn_id` increments exactly once and `parent_state_sha` matches the parent state blob.
- [ ] no `ChatGPT -> ChatGPT` parking transition exists; idle uses `next_actor=null`.

## Scheduler

- [ ] dependencies are enforced.
- [ ] capability-blocked tasks remain blocked until capabilities materially change.
- [ ] QA routes to `qa_actor` and only QA actor may emit `qa_pass` / `qa_fail`.
- [ ] attempts/max-attempts stop infinite loops.

## Binary data plane

- [ ] each manifest is processed independently.
- [ ] a rejected manifest creates `production/import-rejected/<slug>.md` and does not prevent another manifest from being attempted.
- [ ] JPEG integrity requires EOI + Pillow verify/load.
- [ ] import target stays under `content/`.
- [ ] canonical identity cannot be replaced by the normal importer.

## Identity

- [ ] `character/identity.json` records active canonical integrity state.
- [ ] canonical repair only accepts the explicitly verified replacement SHA.
- [ ] normal agent proposals cannot mutate `character/references/` or `character/identity.json`.

## Runtime

- [ ] `coordination-inbox` branch is created from activated `main`.
- [ ] ChatGPT automation is proposal-only and enabled only after v4 is active on `main`.
- [ ] Grok routine reads active `main` protocol every cycle and writes proposal-only after activation.
- [ ] one end-to-end disposable turn succeeds: worker -> inbox proposal -> broker -> canonical state -> QA worker -> broker.

## Repository governance

- [ ] branch/ruleset protection for `main` is enabled in GitHub settings when repository-admin access is available.
- [ ] until then, CI detects invalid coordination transitions and direct agent writes are forbidden by protocol.
