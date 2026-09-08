exec("import argparse,datetime as dt
from pathlib import Path
M={'10_knowledge':('knowledge','k'),'20_projects':('project','p'),'30_workflows':('workflow','w'),'40_skills':('skill','s'),'50_memory':('memory','m')}
def main():
 a=argparse.ArgumentParser(description='Safely add PAIOS frontmatter');a.add_argument('vault',type=Path);a.add_argument('--dry-run',action='store_true');x=a.parse_args();used={line.split(':',1)[1].strip() for f in x.vault.rglob('*.md') for line in f.read_text(encoding='utf-8').splitlines() if line.startswith('id:')}
 today=dt.date.today().isoformat()
 for folder,(typ,pre) in M.items():
  d=x.vault/folder;d.mkdir(parents=True,exist_ok=True)
  for f in sorted(d.glob('*.md')):
   text=f.read_text(encoding='utf-8')
   if text.startswith('---'):continue
   i=1
   while f'{pre}-{today[:4]}-{i:04d}' in used:i+=1
   ident=f'{pre}-{today[:4]}-{i:04d}';used.add(ident);out='---'+chr(10)+'id: '+ident+chr(10)+'type: '+typ+chr(10)+'title: '+f.stem.replace('-',' ')+chr(10)+'created: '+today+chr(10)+'---'+chr(10)+chr(10)+text
   print(('would update ' if x.dry_run else 'update ')+str(f))
   if not x.dry_run:f.write_text(out,encoding='utf-8')
if __name__=='__main__':main()")
