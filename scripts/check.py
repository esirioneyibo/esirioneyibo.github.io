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
for name in ['index.html','en.html','resume.html','resume-fi.html']:
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
 for section in ([] if name.startswith('resume') else ['about','skills','projects','experience','education','contact']): assert section in page.ids
 text=(ROOT/name).read_text()
 assert 'user-scalable=no' not in text and 'contact-form.php' not in text
 assert 'data-width=' not in text
 for field in ['og:title','og:description','og:image','name="description"','rel="canonical"']: assert field in text
 for project in json.loads((ROOT/('data/profile.fi.json' if name in ['index.html','resume-fi.html'] else 'data/profile.json')).read_text())['projects']:
  assert text.count('<h3>'+escape(project[0])+'</h3>')==1, (name,project[0],'missing or duplicate project')
d=json.loads((ROOT/'data/profile.json').read_text())
assert len(d['projects'])==9
assert len({p[0] for p in d['projects']})==9
assert sum(p[1]=='Launched' for p in d['projects'])==1
for p in d['projects']:
 assert p[0] in (ROOT/'resume.txt').read_text()
for group,items in d['skills'].items(): assert len(items)==len(set(items)),group
print('PASS: balanced HTML, unique IDs and projects, local assets, navigation targets, metadata, nine projects, launch status and resume coverage.')

# Guard against partially translated pages and unintentional content loss.
fi=json.loads((ROOT/'data/profile.fi.json').read_text())
for key in ['projects','experience','education','strengths','about']:
 assert len(fi[key])==len(d[key]), ('Finnish content missing',key)
assert [len(x) for x in fi['skills'].values()]==[len(x) for x in d['skills'].values()]
for english,finnish in zip(d['projects'],fi['projects']):
 assert [link[1] for link in english[6]]==[link[1] for link in finnish[6]], 'Project URLs differ by language'
 assert english[1]!=finnish[1] and english[2]!=finnish[2] and english[3]!=finnish[3], 'Untranslated project status, role or description'
for english,finnish in zip(d['experience'],fi['experience']):
 assert english[0]!=finnish[0] and english[3]!=finnish[3], 'Untranslated employment entry'
for filename in ['index.html','resume-fi.html']:
 text=(ROOT/filename).read_text()
 for english in d['projects']:
  assert escape(english[3],quote=True) not in text, (filename,'English project description')
 for content in [*fi['about'],*fi['strengths'],*[x[3] for x in fi['projects']],*[x[3] for x in fi['experience']]]:
  assert escape(content,quote=True) in text, (filename,'Finnish content missing',content)
 assert 'Vakituinen työntekijä' in text
 assert 'project identity placeholder' not in text
 assert 'Valkeakoski, Finland' not in text
 expected_link='href="resume-fi.pdf"' if filename=='resume-fi.html' else 'href="resume-fi.html"'
 assert expected_link in text
assert 'Lataa PDF-ansioluettelo' in (ROOT/'resume-fi.html').read_text()
assert 'Vakituinen työntekijä' in (ROOT/'resume-fi.txt').read_text()
for file in ['resume.pdf','resume-fi.pdf']:
 assert (ROOT/file).read_bytes().startswith(b'%PDF-'), (file,'invalid PDF')
print('PASS: complete Finnish content, equivalent project coverage/URLs, translated employment, Finnish resume downloads and valid PDF files.')
