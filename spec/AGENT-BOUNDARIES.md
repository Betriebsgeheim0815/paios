# PAIOS Agent Boundaries

The agent may change project source, tests, documentation, CI and MCP configuration only inside an isolated feature branch.

The agent must not write directly to main, the production vault, reference-vault, Hermes user settings, or secrets.

Changes to PAIOS business data must be represented as a pending proposal and reviewed before approval.

CI checks protected paths on every pull request.

The user sees the branch, changed files, checks, diff and open review points.

The backend keeps the canonical vault safe through validation, proposals, revision checks and audit events.
