# Coordination v4 inbox

Transport branch: `coordination-inbox`.

Agents create exactly one new `*.json` proposal per mailbox commit. The commit may contain no other changed path. Proposal files are immutable. Canonical state is never written on this branch by an agent.
