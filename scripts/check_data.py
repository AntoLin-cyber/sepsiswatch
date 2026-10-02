from pathlib import Path
import csv
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'/'physionet_2019'; fs=sorted(DATA.glob('*.psv'))
print('PhysioNet folder:',DATA); print('PSV files:',len(fs)); print('Target: 200')
for f in fs[:10]:
    with open(f,encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='|'))
    labels=sum(int(float(r.get('SepsisLabel') or 0)) for r in rows)
    print(f'{f.name}: {len(rows)} hours | positive labels: {labels}')
