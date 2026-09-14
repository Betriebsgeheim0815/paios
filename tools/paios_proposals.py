"""Create and validate safe PAIOS contribution proposals."""
import datetime as dt
import json
import re
import secrets
from pathlib import Path

OPERATIONS = ("create", "update", "archive")
STATUSES = ("pending",)
REQUIRED = ("proposal_id", "entity_id", "operation", "actor", "base_revision", "created_at", "status", "patch", "provenance")
LLOWED = set(REQUIRED) | {"sources", "reason"}

def validate_proposal(proposal):
  if not isinstance(proposal, dict):
    return ["proposal must be an object"]
  errors = []
  errors.extend(f"missing {field}" for field in REQUIRED if field not in proposal)
  errors.extend(f"unexpected field: {field}" for field in set(proposal) - ALLOWED)
  if not re.fullmatch(r"prop-[A-Za-z0-9._-]{1,80}", str(proposal.get("proposal_id", ""))):
    errors.append("proposal_id is not a safe filename")
  if not isinstance(proposal.get("entity_id"), str) or not proposal.get("entity_id").strip():
    errors.append("entity_id must be a non-empty string")
  if proposal.get("operation") not in OPERATIONS:
    errors.append("unsupported operation")
  if not isinstance(proposal.get("actor"), str) or not proposal.get("actor").strip():
    errors.append("actor must be a non-empty string")
  if not isinstance(proposal.get("base_revision"), int) or isinstance(proposal.get("base_revision"), bool) or proposal.get("base_revision") < 0:
    errors.append("base_revision must be a non-negative integer")
  if not isinstance(proposal.get("created_at"), str):
    errors.append("created_at must be an ISO datetime string")
  else:
    try: dt.datetime.fromisoformat(proposal["created_at"])
    except ValueError: errors.append("created_at must be an ISO datetime string")
  if proposal.get("status") not in STATUSES:
    errors.append("unsupported status")
  if not isinstance(proposal.get("patch"), dict):
    errors.append("patch must be an object")
  provenance = proposal.get("provenance")
  if not isinstance(provenance, dict) or not isinstance(provenance.get("actor"), str) or not isinstance(provenance.get("tool"), str) or not isinstance(provenance.get("recorded_at"), str):
    errors.append("provenance must contain actor, tool and recorded_at")
  if "sources" in proposal and (not isinstance(proposal["sources"], list) or not all(isinstance(item, str) for item in proposal["sources"])):
    errors.append("sources must be a list of strings")
  if "reason" in proposal and not isinstance(proposal["reason"], str):
    errors.append("reason must be a string")
  return errors

def create_proposal(entity_id, operation, patch, actor, base_revision, sources=None, reason=""):
  now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
  proposal = {"proposal_id": f"prop-{now[:10]}-{secrets.token_hex(4)}", "entity_id": entity_id, "operation": operation, "actor": actor, "base_revision": base_revision, "created_at": now, "status": "pending", "patch": patch, "sources": list(sources or []), "reason": reason, "provenance": {"actor": actor, "tool": "paios_proposals", "recorded_at": now}}
  errors = validate_proposal(proposal)
  if errors: raise ValueError("; ".join(errors))
  return proposal

def save_proposal(vault, proposal):
  errors = validate_proposal(proposal)
  if errors: raise ValueError("; ".join(errors))
  directory = Path(vault) / "00_meta" / "proposals"
  directory.mkdir(parents=True, exist_ok=True)
  target = directory / f"{proposal['proposal_id']}.json"
  with target.open("x", encoding="utf-8") as handle:
    handle.write(json.dumps(proposal, ensure_ascii=False, indent=2))
  return target

def load_proposals(vault):
  directory = Path(vault) / "00_meta" / "proposals"
  return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]
