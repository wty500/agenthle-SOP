import os, json, shutil, zipfile
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
benchmark_root = Path(os.environ.get('AGENTHLE_BENCHMARK_ROOT', repo_root / 'examples' / 'benchmark_stub'))
out_root = Path(os.environ.get('OPENCLAW_SCALEUP_OUT', repo_root / 'artifacts'))
out_dir = out_root / 'openclaw_scaleup_prompts_bundle_2026-04-04'
out_zip = out_root / 'openclaw_scaleup_prompts_bundle_2026-04-04.zip'

root = benchmark_root

if out_dir.exists():
    shutil.rmtree(out_dir)
out_dir.mkdir(parents=True, exist_ok=True)

# Candidate files: all md/txt/json prompts and review docs relevant to the workflow.
include_files = []
for sub in [root / 'new_tasks', root / 'tasks_to_submit', root / 'scripts']:
    if not sub.exists():
        continue
    for p in sub.rglob('*'):
        if p.is_dir():
            continue
        lower = p.name.lower()
        rel = p.relative_to(root)
        if p.suffix.lower() in {'.md', '.txt', '.json'}:
            if any(k in lower for k in ['prompt', 'audit', 'review', 'shortlist', 'replacement', 'difficulty', 'candidate', 'handoff', 'statistics']) or 'tasks_to_submit' in str(rel).replace('\\','/'):
                include_files.append(p)

# de-dup preserve order
seen = set()
final = []
for p in include_files:
    s = str(p)
    if s not in seen:
        seen.add(s)
        final.append(p)

for src in final:
    dst = out_dir / src.relative_to(root)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

readme = []
readme.append('# OpenClaw Scale-Up Prompts Bundle')
readme.append('')
readme.append('This bundle collects markdown/text/json prompt artifacts used to reproduce the benchmark scale-up workflow in OpenClaw.')
readme.append('')
readme.append('It includes:')
readme.append('- reviewed task prompts and audits')
readme.append('- shortlist / handoff / replacement triage docs')
readme.append('- tasks_to_submit prompt files')
readme.append('- benchmark scripts metadata/prompts/audit docs where applicable')
readme.append('')
readme.append(f'Total files: {len(final)}')
(out_dir / 'README.md').write_text('\n'.join(readme), encoding='utf-8')

manifest = {
    'generated': '2026-04-04',
    'file_count': len(final),
    'files': [str(p.relative_to(root)).replace('\\','/') for p in final],
}
(out_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

if out_zip.exists():
    out_zip.unlink()
with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
    for p in out_dir.rglob('*'):
        zf.write(p, p.relative_to(out_dir))

print(str(out_dir))
print(str(out_zip))
print(len(final))
