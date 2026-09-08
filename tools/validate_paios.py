import datetime as dt, re, sys
from pathlib import Path
REQUIRED_DIRS = ['00_meta', '10_knowledge', '20_projects', '50_memory']
RECOMMENDED_DIRS = ['30_workflows', '40_skills', '90_archive']
REQUIRED_META = ['paios.yaml', 'principles.md']
REQUIRED_FM = ['id', 'type', 'title', 'created']
PREFIXES = {'knowledge': {'k','moc'},'project': {'p'},'workflow': {'w'},'skill': {'s'},'memory': {'m'},'meta': {'doc','moc'},'moc': {'moc'}}
ID_RE = re.compile(r'([a-z]+)-([0-9]{4})-([0-9]+)$')
SECRETS = (r'sk-[A-Za-z0-9]{16,}',r'AIza[0-9A-Za-z_-]{20,}',r'ghp_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'xox[baprs]-[A-Za-z0-9-]{10,}',r'-----BEGIN [A-Z ]*PRIVATE KEY-----')

def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---': return None
    end = next((i for i,line in enumerate(lines[1:],1) if line.strip() == '---'), None)
    if end is None: return None
    data = {}
    for line in lines[1:end]:
        if ':' in line and not line.lstrip().startswith('#'):
            key,value = line.split(':',1); data[key.strip()] = value.strip().strip('\"')
    return data

def valid_id(identifier, kind):
    match = ID_RE.fullmatch(identifier)
    if match: return match.group(1) in PREFIXES.get(kind,set())
    match = re.fullmatch(r'(doc|moc)-[a-z0-9-]+',identifier)
    return bool(match and match.group(1) in PREFIXES.get(kind,set()))

def validate(vault):
    errors,warnings,seen,checked,mocs = [],[],{},0,0
    for directory in REQUIRED_DIRS:
        if not (vault/directory).is_dir(): errors.append('Pflichtordner fehlt: '+directory+'/')
    for directory in RECOMMENDED_DIRS:
        if not (vault/directory).is_dir(): warnings.append('Empfohlener Ordner fehlt: '+directory+'/')
    for filename in REQUIRED_META:
        if not (vault/'00_meta'/filename).is_file(): errors.append('00_meta/'+filename+' fehlt')
    for path in sorted(vault.rglob('*.md')):
        if '.obsidian' in path.parts or '90_archive' in path.parts: continue
        checked += 1; relative = path.relative_to(vault)
        try: text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError: errors.append('Nicht-UTF-8: '+str(relative)); continue
        data = parse_frontmatter(text)
        if data is None: errors.append('Kein gültiges Frontmatter: '+str(relative)); continue
        missing = [field for field in REQUIRED_FM if not data.get(field)]
        if missing: errors.extend([field+' fehlt: '+str(relative) for field in missing]); continue
        identifier,kind = data['id'],data['type']
        if identifier in seen: errors.append('Doppelte id: '+identifier)
        seen[identifier] = relative
        if kind not in PREFIXES or not valid_id(identifier,kind): errors.append('ID passt nicht zu type: '+identifier+' / '+kind)
        try: dt.date.fromisoformat(data['created'])
        except ValueError: errors.append('created ist kein ISO-Datum: '+str(relative))
        if kind == 'project' and data.get('status') not in {'active','paused','done'}: errors.append('Ungültiger project-Status: '+str(relative))
        if kind == 'memory' and data.get('scope') not in {'global','project','user','session'}: errors.append('Ungültiger memory-Scope: '+str(relative))
        if kind == 'moc' or identifier.startswith('moc-'): mocs += 1
        if any(re.search(pattern,text) for pattern in SECRETS): errors.append('Möglicher Secret-Fund: '+str(relative))
    if not (vault/'.git').exists(): warnings.append('Kein Git-Repository; Level 2 empfiehlt Git.')
    if not mocs: warnings.append('Kein MOC gefunden; Level 2 empfiehlt mindestens einen MOC.')
    return errors,warnings,checked

def main():
    if len(sys.argv) != 2: print('Nutzung: python validate_paios.py <vault>'); return 2
    vault = Path(sys.argv[1])
    if not vault.is_dir(): print('Pfad ist kein Verzeichnis: '+str(vault)); return 2
    errors,warnings,checked = validate(vault)
    print('PAIOS-Validierung: '+str(vault)); print('Geprüfte Dateien: '+str(checked))
    for item in warnings: print('[WARN] '+item)
    for item in errors: print('[FEHLER] '+item)
    print('Ergebnis: '+('NICHT konform' if errors else 'Level 1 KONFORM'))
    return 1 if errors else 0
if __name__ == '__main__': raise SystemExit(main())
