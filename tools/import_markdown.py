#!/usr/bin/env python3
import argparse,datetime as dt,re
from pathlib import Path

TYPE_TO_FOLDER = {'knowledge':'10_knowledge','project':'20_projects','memory':'50_memory'}

def main():
    p=argparse.ArgumentParser(description='Import plain Markdown conservatively')
    p.add_argument('source',type=Path); p.add_argument('vault',type=Path); p.add_argument('--type',choices=TYPE_TO_FOLDER,default='knowledge')
    a=p.parse_args(); folder=a.vault/TYPE_TO_FOLDER[a.type]; folder.mkdir(parents=True,exist_ok=True)
    today=dt.date.today().isoformat(); used={int(m.group(1)) for m in (re.search(r'-\d{4}-(\d{4})$',p.name) for p in folder.glob('*.md')) if m}
    n=max(used or {0})+1; prefix={'knowledge':'k','project':'p','memory':'m'}[a.type]; target=folder/f'{prefix}-{today[:4]}-{n:04d}.md'
    text=a.source.read_text(encoding='utf-8'); title=a.source.stem.replace('_',' ')
    if not text.lstrip().startswith('---'): text=f'---\n id: {target.stem}\n type: {a.type}\n title: "{title}"\n created: {today}\n---\n\n'+text
    target.write_text(text,encoding='utf-8'); print(target)

if __name__=='__main__': main()
