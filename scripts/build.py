"""Generate static bilingual portfolio and resume from confirmed shared content. Python 3, no dependencies."""
from pathlib import Path
import json
from html import escape as e
ROOT=Path(__file__).resolve().parents[1]
profiles={lang:json.loads((ROOT/file).read_text()) for lang,file in [('en','data/profile.json'),('fi','data/profile.fi.json')]}
d=profiles['en']
def esc(s): return e(str(s),quote=True)
def tags(items): return '<ul class="tags">'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</ul>'
def para(items): return ''.join('<p>'+esc(x)+'</p>' for x in items)
def experience(): return ''.join('<article class="timeline-item"><span class="eyebrow">'+esc(x[2])+'</span><h3>'+esc(x[0])+'</h3><p class="organization">'+esc(x[1])+'</p><p>'+esc(x[3])+'</p></article>' for x in d['experience'])
def education(): return ''.join('<article class="panel"><h3>'+esc(x[0])+'</h3><p>'+esc(x[1])+'</p><p class="muted">'+esc(x[2])+'</p></article>' for x in d['education'])
def skills(): return ''.join('<article class="panel"><h3>'+esc(k)+'</h3>'+tags(v)+'</article>' for k,v in d['skills'].items())
def projects(fi=False):
 out=''
 for i,p in enumerate(d['projects']):
  name,status,role,description,stack,features,links=p
  media='<div class="project-visual" role="img" aria-label="'+esc(name)+(' – projektin paikkamerkkikuva' if fi else ' project identity placeholder')+'"><span class="visual-number">0'+str(i+1)+'</span><strong>'+esc(name)+'</strong><span>'+('Projektin kuvitus · ei kuvakaappaus' if fi else 'Project identity · screenshot pending')+'</span></div>'
  out+='<article class="project panel" id="project-'+str(i+1)+'">'+media+'<div class="project-copy"><span class="status">'+esc(status)+'</span><h3>'+esc(name)+'</h3><p class="organization">'+esc(role)+'</p><p>'+esc(description)+'</p>'+tags(stack)
  if features: out+='<details><summary>'+('Projektin tiedot' if fi else 'Project details')+'</summary><ul>'+''.join('<li>'+esc(x)+'</li>' for x in features)+'</ul></details>'
  out+='<div class="project-links">'+''.join('<a href="'+esc(url)+'">'+esc(label)+' ↗</a>' for label,url in links)+'</div></div></article>'
 return out

def head(lang,title,description,path):
 fi=lang=='fi'
 resume=path.startswith('resume')
 fi_url='resume-fi.html' if resume else ''
 en_url='resume.html' if resume else 'en.html'
 card='social-card-fi.png' if fi else 'social-card.png'
 return '<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>'+esc(title)+'</title><meta name="description" content="'+esc(description)+'"><meta name="theme-color" content="#101927"><link rel="icon" href="favicon.ico"><link rel="canonical" href="https://esirioneyibo.github.io/'+path+'"><link rel="alternate" hreflang="fi" href="https://esirioneyibo.github.io/'+fi_url+'"><link rel="alternate" hreflang="en" href="https://esirioneyibo.github.io/'+en_url+'"><meta property="og:locale" content="'+('fi_FI' if fi else 'en_GB')+'"><meta property="og:type" content="website"><meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(description)+'"><meta property="og:url" content="https://esirioneyibo.github.io/'+path+'"><meta property="og:image" content="https://esirioneyibo.github.io/img/'+card+'"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="css/portfolio.css"></head><body>'
for fi in [True,False]:
 lang='fi' if fi else 'en'; path='index.html' if fi else 'en.html'
 d=profiles[lang]
 resume_path='resume-fi.html' if fi else 'resume.html'
 labels=['Tietoa','Osaaminen','Projektit','Kokemus','Koulutus','Yhteystiedot'] if fi else ['About','Skills','Projects','Experience','Education','Contact']
 ids=['about','skills','projects','experience','education','contact']
 title='James Oneyibo | '+('Ohjelmistokehittäjä & automaatioinsinööri' if fi else d['title'])
 s=head(lang,title,'Ohjelmistokehitys, automaatio ja käytännön digitaaliset ratkaisut. James Oneyibo, Suomi.' if fi else d['intro'],'' if fi else path)
 s+='<a class="skip" href="#main">'+('Siirry sisältöön' if fi else 'Skip to content')+'</a><header class="site-header"><a class="brand" href="'+path+'"><span class="brand-mark">JO<span>.</span></span> James Oneyibo</a><nav aria-label="'+('Päänavigaatio' if fi else 'Main navigation')+'">'+''.join('<a href="#'+i+'">'+l+'</a>' for i,l in zip(ids,labels))+'</nav><a class="language" href="'+('en.html' if fi else 'index.html')+'" lang="'+('en' if fi else 'fi')+'">'+('English' if fi else 'Suomi')+'</a></header>'
 headline=d['headline']
 intro=d['intro']
 s+='<main id="main"><section class="hero"><div><p class="eyebrow">'+('SUOMI / OHJELMISTOT / AUTOMAATIO' if fi else 'FINLAND / SOFTWARE / AUTOMATION')+'</p><p class="hero-title">'+('Ohjelmistokehittäjä & automaatioinsinööri' if fi else d['title'])+'</p><h1>'+esc(headline)+'</h1><p class="lead">'+esc(intro)+'</p><p class="secondary">'+esc(d['secondary'])+'</p><div class="actions"><a class="button" href="#projects">'+('Tutustu projekteihin' if fi else 'Explore my work')+' ↗</a><a class="button outline" href="'+resume_path+'">'+('Ansioluettelo' if fi else 'View resume')+'</a></div></div><aside class="hero-aside"><span class="eyebrow">JAMES ONEYIBO</span><div class="monogram" aria-hidden="true">J<span>O</span></div><p>'+('Insinööritausta.<br>Ohjelmistokehittäjän ajattelutapa.<br>Ihmislähtöinen näkökulma.' if fi else 'Engineering foundation.<br>Software mindset.<br>Human perspective.')+'</p><span class="location">Valkeakoski · '+('Suomi' if fi else 'Finland')+'</span></aside></section>'
 stats=['13+ vuotta itsenäistä ohjelmistokehitystä ja oppimista','9 dokumentoitua teknologiaprojektia, myös konsepteja','1 julkaistu Android-tuote','Tuotekehitys ja lokalisointi englanniksi ja suomeksi'] if fi else ['13+ years of independent development & learning','9 documented technology projects, including concepts','1 confirmed launched Android product','EN / FI product development & localization']
 s+='<div class="stats">'+''.join('<p>'+esc(x)+'</p>' for x in stats)+'</div>'
 about=d['about']
 sections=[para(about)+'<p class="muted">'+('Kielet: englanti (äidinkieli), suomi: suullinen hyvä, kirjallinen tyydyttävä. Vapaa-ajalla vapaaehtoistoimintaa sekä ulkoilua ja retkeilyä perheen kanssa.' if fi else 'Languages: English (native); Finnish: good spoken, satisfactory written. Outside technology: volunteering, outdoor activities and hiking with family.')+'</p>'+tags(d['strengths']),'<div class="grid skills">'+skills()+'</div>','<p class="section-intro">'+('Julkaistut tuotteet, kehitysprojektit ja konseptit on merkitty erikseen. Projektikuvitukset ovat paikkamerkkejä.' if fi else 'Launched products, work in progress and concepts. Project identity artwork is a placeholder, not a product screenshot.')+'</p><div class="grid projects">'+projects(fi)+'</div>','<div class="timeline">'+experience()+'</div>','<div class="grid">'+education()+'</div>','<div class="contact-panel"><h3>'+('Rakennetaan jotain hyödyllistä.' if fi else 'Let’s build something useful.')+'</h3><p>'+('Ohjelmistokehitys, toimeksiannot, kumppanuudet ja yhteistyö.' if fi else 'Software development opportunities, freelance projects, business partnerships and collaboration.')+'</p><div class="actions"><a class="button" href="mailto:esirioneyibo@gmail.com">esirioneyibo@gmail.com ↗</a><a href="https://github.com/esirioneyibo">GitHub ↗</a><a href="tel:+358456726453">+358 45 672 6453</a></div><p class="muted">Valkeakoski, '+('Suomi' if fi else 'Finland')+'</p></div>']
 for num,(i,l,content) in enumerate(zip(ids,labels,sections),1):
  s+='<section class="section" id="'+i+'"><div class="section-heading"><span class="eyebrow">0'+str(num)+' /</span><h2>'+l+'</h2></div>'+content+'</section>'
 s+='</main><footer><span>© 2026 James Oneyibo</span><a href="'+resume_path+'">'+('Ansioluettelo' if fi else 'Resume')+'</a><a href="#main">'+('Takaisin ylös' if fi else 'Back to top')+' ↑</a></footer></body></html>\n'
 (ROOT/path).write_text(s.replace('><', '>\n<'))
for fi in [False, True]:
 lang='fi' if fi else 'en'
 d=profiles[lang]
 stem='resume-fi' if fi else 'resume'
 portfolio='index.html' if fi else 'en.html'
 headings=['Profiili','Tekninen osaaminen','Projektit','Työkokemus','Koulutus','Vahvuudet','Kielet ja kiinnostuksen kohteet'] if fi else ['Profile','Technical skills','Projects','Experience','Education','Strengths','Languages & interests']
 languages='Englanti: äidinkieli. Suomi: hyvä suullinen ja tyydyttävä kirjallinen taito. Tuotekehitys ja lokalisointi englanniksi ja suomeksi. Vapaaehtoistoiminta, ulkoilu ja retkeily perheen kanssa.' if fi else 'English: native. Finnish: good spoken, satisfactory written. English/Finnish product development and localization. Volunteering, outdoor activities and hiking with family.'
 location='Valkeakoski, Suomi' if fi else 'Valkeakoski, Finland'
 s=head(lang,'James Oneyibo | '+('Ansioluettelo' if fi else 'Professional Resume'),d['title'],stem+'.html')
 s+='<header class="resume-header"><a href="'+portfolio+'">← '+('Takaisin portfolioon' if fi else 'Portfolio')+'</a><a href="'+stem+'.pdf" download>'+('Lataa PDF-ansioluettelo' if fi else 'Download PDF resume')+'</a><a href="'+stem+'.txt" download>'+('Lataa ansioluettelo tekstinä' if fi else 'Download text resume')+'</a><button type="button" id="print-resume">'+('Tulosta / Tallenna PDF-tiedostona' if fi else 'Print / Save as PDF')+'</button><a class="language" href="'+('resume.html' if fi else 'resume-fi.html')+'" lang="'+('en' if fi else 'fi')+'">'+('English' if fi else 'Suomi')+'</a></header>'
 s+='<main class="resume"><h1>'+esc(d['name'])+'</h1><p class="lead">'+esc(d['title'])+'</p><p>'+esc(d['secondary'])+'</p><p>'+location+' · <a href="mailto:esirioneyibo@gmail.com">esirioneyibo@gmail.com</a> · <a href="tel:+358456726453">+358 45 672 6453</a> · <a href="https://github.com/esirioneyibo">GitHub</a></p>'
 contents=[para(d['about']),skills(),projects(fi),experience(),education(),tags(d['strengths']),para([languages])]
 for heading,content in zip(headings,contents): s+='<h2>'+heading+'</h2>'+content
 s+='</main><script src="js/resume.js" defer></script></body></html>'
 (ROOT/(stem+'.html')).write_text(s.replace('><', '>\n<'))
 lines=[d['name'],d['title'],d['secondary'],location+' | esirioneyibo@gmail.com | +358 45 672 6453','https://github.com/esirioneyibo',headings[0].upper(),*d['about'],headings[1].upper()]
 lines += [k+': '+', '.join(v) for k,v in d['skills'].items()]
 lines += [headings[2].upper()]
 for project in d['projects']: lines += [project[0]+' | '+project[1]+' | '+project[2],project[3],', '.join(project[4]),*project[5],*[label+': '+url for label,url in project[6]]]
 lines += [headings[3].upper(),*[' | '.join(x) for x in d['experience']],headings[4].upper(),*[' | '.join(x) for x in d['education']],headings[5].upper(),', '.join(d['strengths']),headings[6].upper(),languages]
 (ROOT/(stem+'.txt')).write_text('\n\n'.join(x for x in lines if x)+'\n')
print('Generated Finnish and English portfolios and HTML/text resumes.')
