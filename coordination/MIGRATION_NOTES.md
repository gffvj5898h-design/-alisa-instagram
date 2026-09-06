# Coordination v4 activation / rollback

## Activation

1. Merge the reviewed `coordination-v4` branch to `main` only after PR CI passes.
2. Create/reset `coordination-inbox` from the activated `main` commit.
3. Do not let product agents write canonical state. ChatGPT and Grok create exactly one new `coordination/inbox/*.json` proposal on `coordination-inbox` when they own the turn.
4. Broker workflow validates the proposal against the exact current state blob and applies the canonical transition to `main`.
5. Run one disposable two-agent end-to-end handoff before normal production tasks resume.
6. Enable/update ChatGPT automation only after the disposable handoff passes.

## Rollback

If v4 activation fails before a successful production turn:

- disable ChatGPT v4 automation;
- stop Grok proposal writes;
- do not force-push `main`;
- revert the v4 migration merge commit with a normal Git revert/PR;
- preserve all immutable proposal/message audit files;
- diagnose from GitHub Actions logs and the last valid canonical state.

Never restore v2 by manually editing `coordination/state.json` in-place after v4 has accepted production turns. Use an explicit migration/recovery transaction instead.
