import argparse,re,sys
from datetime import date
from pathlib import Path
FOLDERS = {'10_knowledge': 'k', '20_projects': 'p', '30_workflows': 'w', '40_skills': 's', '50_memory': 'm'}
TYPES = {'k': 'knowledge', 'p': 'project', 'w': 'workflow', 's': 'skill', 'm': 'memory'}
ID_RE = re.compile(r'([a-z]+)-([0-9]{4})-([0-9]+)')

def read_ids(root):
    ids = []
    for path in root.rglob('*.md'):
        ids.extend(re.findall(r'^id:\s*([^\s#]+)',path.read_text(encoding='utf-8'),re.M))
    return ids

def next_id(prefix,year,used):
    number = 0
    for item in used:
        match = ID_RE.fullmatch(item)
        if match and match.group(1) == prefix and match.group(2) == str(year): number = max(number,int(match.group(3)))
    while True:
        number += 1
        candidate = f'{prefix}-{year}-{number:04d}'
        if candidate not in used: used.add(candidate); return candidate

def backfill(root,dry_run=False):
    ids = read_ids(root)
    duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if duplicates: raise ValueError('Bestehende doppelte IDs: '+', '.join(duplicates))
    used = set(ids); today = date.today(); changed = 0
    for path in sorted(root.rglob('*.md')):
        text = path.read_text(encoding='utf-8')
        if text.lstrip().startswith('---'): continue
        prefix = next((p for folder,p in FOLDERS.items() if folder in path.parts),None)
        if not prefix: continue
        identifier = next_id(prefix,today.year,used)
        title = re.sub(r'[^a-zA-Z0-9]+',' ',path.stem).strip() or 'entry'
        frontmatter = '---\n'+'id: '+identifier+'\ntype: '+TYPES[prefix]+'\ntitle: '+title+'\ncreated: '+today.isoformat()+'\n---\n\n'
        if dry_run: print('Would update '+str(path)+' with '+identifier)
        else: path.write_text(frontmatter+text,encoding='utf-8')
        changed += 1
    return changed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add PAIOS frontmatter without ID collisions.')
    parser.add_argument('vault',type=Path); parser.add_argument('--dry-run',action='store_true')
    args = parser.parse_args()
    try: print('Updated: '+str(backfill(args.vault,args.dry_run)))
    except ValueError as error: print('ERROR: '+str(error)); sys.exit(1)
