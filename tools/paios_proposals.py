import datetime as dt
import json
import secrets
from pathlib import Path

OPERATIONS = ("create","update","archive")

def validate_proposal(p):
    errors = []
    for field in ("proposal_id","entity_id","operation","actor","base_revision","created_at","status","patch"):
        if field not in p: errors.append(f"missing field: {field}")
    if not str(p.get("proposal_id","")).startswith("prop-"): errors.append("proposal_id must start with prop-")
    if p.get("operation") not in OPERATIONS: errors.append("unsupported operation")
    if not isinstance(p.get("base_revision"), int) or p.get("base_revision") < 0: errors.append("base_revision must be a non-negative integer")
    if not isinstance(p.get("patch"), dict): errors.append("patch must be an object")
    return errors

def create_proposal(entity_id, operation, patch, actor, base_revision, sources=None, reason=""):
    now = dt.datetime.now(dt.timezone.utc)
    p = {"proposal_id": f"prop-{now.strftime('%Y-%m-%d')}-{secrets.token_hex(4)}","entity_id":entity_id,"operation":operation,"actor":actor,"base_revision":base_revision,"created_at":now.strftime("%Y-%m-%dT%H:%M:%SZ"),"status":"pending","patch":patch,"sources":list(sources or []),"reason":reason}
    errors = validate_proposal(p)
    if errors: raise ValueError("; ".join(errors))
    return p

def save_proposal(vault, proposal):
    errors = validate_proposal(proposal)
    if errors: raise ValueError("; ".join(errors))
    directory = Path(vault) / "00_meta" / "proposals"
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{proposal['proposal_id']}.json"
    if target.exists(): raise FileExistsError(target)
    target.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    return target
