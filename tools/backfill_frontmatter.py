#!/usr/bin/env python3
import argparse,datetime as dt,re
from pathlib import Path

FOLDERS={'10_knowledge':'k','20_projects':'p','30_workflows':'w','40_skills':'s','50_memory':'m'}
ID_RE=re.compile(r'^id:\s*([^\s#]+)',re.M)

def main():
  p=argparse.ArgumentParser(description='Collision-safe PAIOS frontmatter backfill')
  p.add_argument('vault',type=Path); p.add_argument('--dry-run',action='store_true'); a=p.parse_args()
  ids=[]
  for f in a.vault.rglob('*.md'):
    ids+=ID_RE.findall(f.read_text(encoding='utf-8'))
  dups={x for x in ids if ids.count(x)>1}
  if dups: raise SystemExit('Bestehende ID-Kollisionen: '+', '.join(sorted(dups)))
  used=set(ids); year=dt.date.today().year
  for folder,prefix in FOLDERS.items():
    for f in sorted((a.vault/folder).glob('*.md')):
      text=f.read_text(encoding='utf-8')
      if text.lstrip().startswith('---'): continue
      n=1
      while f'{prefix}-{year}-{n:04d}' in used: n+=1
      ident=f'{prefix}-{year}-{n:04d}'; used.add(ident)
      title=f.stem.replace('-',' ').replace('_',' ')
      front=f'---\nid: {ident}\nttype: {{'knowledge':'knowledge','project':'project','workflows':'workflow','skills':'skill','memory':'memory'}.get(folder.split('_')[1],'knowledge')}\ntitle: "{title}"\ncreated: {dt.date.today().isoformat()}\n---\n\n'
      print('DRY-RUN ' if a.dry_run else 'WRITE ',f,ident)
      if not a.dry_run: f.write_text(front+text,encoding='utf-8')
if __name__=='__main__': main()
