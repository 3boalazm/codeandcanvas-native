from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import json,subprocess
root=Path.cwd()
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.jsons=[];self.ld=False;self.buf=''
 def handle_starttag(self,t,a):
  a=dict(a);self.tags.append((t,a))
  if t=='script' and a.get('type')=='application/ld+json':self.ld=True;self.buf=''
 def handle_data(self,d):
  if self.ld:self.buf+=d
 def handle_endtag(self,t):
  if t=='script' and self.ld:self.jsons.append(json.loads(self.buf));self.ld=False
files=[root/'index.html',root/'404.html']+[f for f in root.glob('**/index.html') if not {'docs','dist','node_modules'}.intersection(f.relative_to(root).parts) and f!=root/'index.html']
results=[]
for f in sorted(files):
 p=Parser();p.feed(f.read_text());types=[]
 def walk(x):
  if isinstance(x,dict):
   if '@type' in x:types.append(x['@type'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 for x in p.jsons:walk(x)
 links=[a for t,a in p.tags if t=='a'];ids=[a['id']for t,a in p.tags if 'id'in a];metas={a.get('name',a.get('property')):a.get('content')for t,a in p.tags if t=='meta'}
 results.append({'file':str(f.relative_to(root)),'jsonldTypes':types,'h1':sum(t=='h1'for t,a in p.tags),'duplicateIds':[k for k,v in Counter(ids).items()if v>1],'ogImage':metas.get('og:image'),'robots':metas.get('robots'),'hreflang':sum('hreflang'in a for t,a in p.tags),'placeholderSlots':sum('data-slot'in a for t,a in p.tags),'trackedLinks':sum('data-track'in a for a in links),'totalLinks':len(links),'contactLinks':[(a['href'],a.get('data-track'))for a in links if a.get('href','').startswith('/contact/')],'forms':[{k:v for k,v in a.items()if k.startswith('data-')}for t,a in p.tags if t=='form']})
summary={'pages':len(results),'jsonldPages':sum(bool(x['jsonldTypes'])for x in results),'ogPages':sum(bool(x['ogImage'])for x in results),'hreflangPages':sum(bool(x['hreflang'])for x in results),'placeholderSlots':sum(x['placeholderSlots']for x in results),'trackedLinks':sum(x['trackedLinks']for x in results),'totalLinks':sum(x['totalLinks']for x in results),'fontsBytes':sum(f.stat().st_size for f in (root/'assets/fonts').glob('*')if f.is_file())}
(root/'docs/audit/verification-2026-10-14/evidence/static-results.json').write_text(json.dumps({'summary':summary,'pages':results},indent=2,ensure_ascii=False))
print(summary)
for x in results:
 if x['file'] in ['index.html','about/index.html','services/index.html','technology-services/index.html','creative-services/index.html','healthcare/index.html','pricing-faq/index.html','login/index.html','account/index.html']:print(x)
