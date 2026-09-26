"""Regenerates research.html from tools/papers.json.
Links to files in papers/ are shown only when the file exists, so the live site has no broken links.
Run from the site folder:  python tools/build.py"""
import json, os, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
papers = json.load(open(os.path.join(ROOT, 'tools', 'papers.json'), encoding='utf-8'))
missing = []
def ok(u):
    if u and u.startswith('papers/'):
        if os.path.exists(os.path.join(ROOT, u)): return True
        missing.append(u); return False
    return bool(u)
def item(p):
    t = html.escape(p['title'])
    title = f'<a href="{p["url"]}">{t}</a>' if ok(p['url']) else t
    ex = [f'<a href="{u}">{html.escape(l)}</a>' for l, u in p['extras'] if ok(u)]
    links = f'<div class="links">{" ".join(ex)}</div>' if ex else ''
    return f'  <div class="paper">\n    <div class="title">{title}</div>\n    <div class="info">{p["info"]}</div>\n    {links}\n  </div>'
pubs = '\n'.join(item(p) for p in papers if p['sec'] == 'pub')
wps = '\n'.join(item(p) for p in papers if p['sec'] == 'wp')
tpl = open(os.path.join(ROOT, 'tools', 'research_template.html'), encoding='utf-8').read()
open(os.path.join(ROOT, 'research.html'), 'w', encoding='utf-8', newline='\n').write(
    tpl.replace('{{PUBLICATIONS}}', pubs).replace('{{WORKING_PAPERS}}', wps))
print(f'research.html written: {len(papers)} papers; {len(missing)} linked files not yet in papers/')
open(os.path.join(ROOT, 'tools', 'missing_files.txt'), 'w').write('\n'.join(sorted(set(m[7:] for m in missing))) + '\n')
