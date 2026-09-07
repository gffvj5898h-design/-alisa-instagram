# Coordination v4 human intake

Human product briefs enter the control plane through a dedicated `coordination-intake` branch. A human intake is not an agent turn and must never be emulated by ChatGPT or Grok.

## Transport

- branch: `coordination-intake`
- path: `coordination/intake/*.json`
- one commit = exactly one newly added intake JSON and no other path
- GitHub Actions validates and applies the intake to canonical `main`
- the intake writer may add new structured tasks plus human-authored context files under `content/briefs/` or `content/reels/`
- the workflow serializes with the same `alisa-main-writer` concurrency group as the broker and binary importers

## Intake contract

```json
{
  "schema_version": 1,
  "intake_id": "human-unique-id",
  "summary": "short human intent",
  "tasks": [],
  "context_files": [
    {"path": "content/reels/example/brief.md", "content": "human brief"}
  ]
}
```

Every task must have the normal v4 task fields. Optional `capability_probe` metadata is allowed only on a task that is explicitly intended to verify one actor capability:

```json
"capability_probe": {
  "actor": "grok",
  "capability": "identity_reference_still_generation"
}
```

The probe itself must not require the capability it is testing. A probe may become canonical only after its configured QA actor returns `qa_pass`; then the broker enables that exact capability for that exact actor. This prevents an agent from self-asserting a new capability.

## Safety

- intake is accepted only while canonical state is idle; it never preempts an active agent turn
- task IDs must be new and unique
- dependencies must resolve to existing or same-intake task IDs
- context files are UTF-8 text only
- canonical identity, coordination code/state, workflows and executable production code are not writable through an intake payload
- duplicate intake IDs are rejected
