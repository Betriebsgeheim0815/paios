# PAIOS Agent Boundaries

The agent may change project source, tests, documentation, CI and MCP configuration only inside an isolated feature branch.

The agent must not write directly to main, a production/private vault, Hermes user settings, or secrets.

The versioned `reference-vault/` contains public test fixtures. It may change in an isolated
feature branch when the validator and behavior tests pass; it must never contain private data.

Changes to PAIOS business data must be represented as a pending proposal and reviewed before approval.

CI checks private paths and credentials on every pull request. Separate validation verifies the
public reference vault.

The user sees the branch, changed files, checks, diff and open review points.

The backend keeps the canonical vault safe through validation, proposals, revision checks and audit events.
