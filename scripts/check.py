"""Dependency-free structural and content checks for generated portfolio pages."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, unquote
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,path):
  super().__init__(convert_charrefs=True); self.path=path; self.ids=[]; self.links=[]; self.h1=0; self.stack=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a: self.ids.append(a['id'])
  if tag=='h1': self.h1+=1
  for key in ['href','src']:
   if key in a: self.links.append(a[key])
  if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.stack.append(tag)
 def handle_endtag(self,tag):
  assert self.stack and self.stack.pop()==tag, (self.path,tag,'unbalanced HTML')
pages={}
for name in ['index.html','en.html','resume.html']:
 page=Page(name); page.feed((ROOT/name).read_text()); pages[name]=page
 assert not page.stack, (name,'unclosed tags')
 assert len(page.ids)==len(set(page.ids)), (name,'duplicate IDs')
 assert page.h1==1, (name,'expected one h1')
for name,page in pages.items():
 for url in page.links:
  p=urlsplit(url)
  if p.scheme or p.netloc: continue
  target=(ROOT/unquote(p.path)) if p.path else ROOT/name
  assert target.is_file(), (name,'missing local target',url)
  if p.fragment:
   dest=pages.get(target.name)
   assert dest and p.fragment in dest.ids, (name,'broken fragment',url)
 for section in ([] if name=='resume.html' else ['about','skills','projects','experience','education','contact']): assert section in page.ids
 text=(ROOT/name).read_text()
 assert 'user-scalable=no' not in text and 'contact-form.php' not in text
 assert 'data-width=' not in text
 for field in ['og:title','og:description','og:image','name="description"','rel="canonical"']: assert field in text
 for project in json.loads((ROOT/'data/profile.json').read_text())['projects']:
  assert text.count('<h3>'+escape(project[0])+'</h3>')==1, (name,project[0],'missing or duplicate project')
d=json.loads((ROOT/'data/profile.json').read_text())
assert len(d['projects'])==9
assert len({p[0] for p in d['projects']})==9
assert sum(p[1]=='Launched' for p in d['projects'])==1
for p in d['projects']:
 assert p[0] in (ROOT/'resume.txt').read_text()
for group,items in d['skills'].items(): assert len(items)==len(set(items)),group
print('PASS: balanced HTML, unique IDs and projects, local assets, navigation targets, metadata, nine projects, launch status and resume coverage.')
