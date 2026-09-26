#!/usr/bin/env python3
"""Read-only PAIOS vault adapter."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from paios_core import PaiosError, find_entry, iter_entries  # noqa: E402


def search(vault, query: str) -> int:
    needle = query.casefold()
    output = []
    for entry in iter_entries(vault, strict=False):
        if needle in entry.text.casefold():
            output.append(
                {
                    "path": entry.relative.as_posix(),
                    "id": entry.metadata.get("id"),
                    "title": entry.metadata.get("title"),
                    "snippet": " ".join(entry.body.split())[:240],
                }
            )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def read_entry(vault, identifier: str) -> int:
    entry = find_entry(vault, identifier, strict=False)
    if entry is None:
        print("Not found", file=sys.stderr)
        return 1
    print(entry.text, end="" if entry.text.endswith("\n") else "\n")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vault")
    commands = parser.add_subparsers(dest="command", required=True)
    find = commands.add_parser("search")
    find.add_argument("query")
    read = commands.add_parser("read")
    read.add_argument("id")
    args = parser.parse_args(argv)
    try:
        return search(args.vault, args.query) if args.command == "search" else read_entry(args.vault, args.id)
    except (PaiosError, OSError, UnicodeError) as error:
        print(f"Adapter error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
