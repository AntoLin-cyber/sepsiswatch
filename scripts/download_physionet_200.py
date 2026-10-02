from pathlib import Path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[1]; DEST=ROOT/'data'/'physionet_2019'; DEST.mkdir(parents=True,exist_ok=True)
BASE='https://physionet.org/content/challenge-2019/1.0.0/training/training_setA/'
s=requests.Session(); s.headers['User-Agent']='Mozilla/5.0 SepsisWatch Dataset Downloader'
print('Checking PhysioNet:',BASE)
r=s.get(BASE,timeout=30); r.raise_for_status(); soup=BeautifulSoup(r.text,'html.parser')
files={}
for a in soup.find_all('a'):
    href=a.get('href','')
    if href.lower().endswith('.psv'):
        url=urljoin(r.url,href); files[Path(url.split('?')[0]).name]=url
items=sorted(files.items())[:200]
print('Unique files found:',len(files)); print('Target:',len(items))
for i,(name,url) in enumerate(items,1):
    out=DEST/name
    if out.exists() and out.stat().st_size>100: print(f'[{i:03}/{len(items):03}] EXISTS   {name}'); continue
    try:
        print(f'[{i:03}/{len(items):03}] DOWNLOAD {name}')
        x=s.get(url,timeout=60); x.raise_for_status()
        if len(x.content)<100: raise RuntimeError('file too small')
        out.write_bytes(x.content); print(f'          OK ({len(x.content)/1024:.1f} KB)')
    except Exception as e: print('          FAILED:',e)
actual=list(DEST.glob('*.psv')); print('\nFiles in folder:',len(actual)); print('Target: 200')
if len(actual)>=200: print('SUCCESS: 200 files ready.')
else: print(f'PARTIAL: {len(actual)} files available.')
