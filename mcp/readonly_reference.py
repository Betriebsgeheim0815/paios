#!/usr/bin/env python3
import argparse
from pathlib import Path

def entries(root):
    return (root.resolve()).rglob('*.md')

def read_entry(root, entry_id):
    for path in entries(root):
        text = path.read_text(encoding='utf-8')
        if f'id: {entry_id}' in text.split('---', 2)[0]:
            return text
    return None

def search(root, query):
    q = query.casefold()
    return [str(p.relative_to(root)) for p in entries(root) if q in p.read_text(encoding='utf-8').casefold()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read-only PAIOS adapter')
    parser.add_argument('root', type=Path)
    parser.add_argument('operation', choices=['read', 'search'])
    parser.add_argument('value')
    args = parser.parse_args()
    result = read_entry(args.root, args.value) if args.operation == 'read' else '\n'.join(search(args.root, args.value))
    print(result or 'Not found')
