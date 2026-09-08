#!/usr/bin/env python3
import argparse
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description='Build a small project context')
    p.add_argument('vault',type=Path); p.add_argument('project_id'); a=p.parse_args()
    all_files=list(a.vault.rglob('*.md')); project=next((x for x in all_files if f'id: {a.project_id}' in x.read_text(encoding='utf-8')),None)
    if not project: raise SystemExit('Project not found')
    text=project.read_text(encoding='utf-8'); print(text)
    for x in all_files:
        if x==project: continue
        other=x.read_text(encoding='utf-8')
        if a.project_id in other or x.stem in text: print('\n'+other)

if __name__=='__main__': main()
