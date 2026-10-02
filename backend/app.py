from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
from datetime import datetime
import sqlite3, csv, glob, random, os

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / 'dashboard'
DATA = ROOT / 'data' / 'physionet_2019'
DB = ROOT / 'data' / 'sepsiswatch.db'

app = Flask(__name__, static_folder=None)

DOCTORS = [
    {'id':'D01','name':'Dr. Ananya Rao','specialty':'Critical Care','nurses':['N01','N02']},
    {'id':'D02','name':'Dr. Daniel Thomas','specialty':'Internal Medicine','nurses':['N03']},
]
NURSES = [
    {'id':'N01','name':'Nurse Meera','shift':'ICU Day','doctor':'D01','patient_count':10},
    {'id':'N02','name':'Nurse Kavya','shift':'ICU Evening','doctor':'D01','patient_count':10},
    {'id':'N03','name':'Nurse Arjun','shift':'Ward Day','doctor':'D02','patient_count':10},
]

names = [
('P001','Aarav Menon',62,'ICU-04','N01',.86,.21,118,91,38.8,92,27,.91,'Respiratory deterioration'),
('P002','Meera Shah',54,'ICU-05','N01',.72,.13,109,93,38.1,99,24,.85,'Rising heart rate'),
('P003','Rahul Nair',71,'ICU-06','N01',.57,.08,101,95,37.9,106,22,.79,'Trend changed'),
('P004','Ishita Roy',43,'ICU-08','N01',.18,-.02,77,98,36.8,122,16,.96,'No active alert'),
('P005','Vikram Das',68,'ICU-11','N01',.81,.17,114,92,38.5,95,26,.88,'Risk accelerating'),
('P006','Sara Joseph',35,'ICU-12','N01',.49,.05,96,96,37.7,110,21,.82,'Data change detected'),
('P007','Kabir Ali',59,'ICU-13','N01',.67,.11,105,94,38.0,101,23,.86,'Oxygen trend'),
('P008','Nisha Kumar',47,'ICU-14','N01',.24,-.01,82,98,36.9,119,17,.95,'Stable trend'),
('P009','Arun Patel',76,'ICU-15','N01',.89,.24,121,90,39.0,88,29,.83,'Multi-signal deterioration'),
('P010','Diya Thomas',29,'ICU-16','N01',.42,.04,94,97,37.5,113,20,.90,'Mild change'),
('P011','Riya Menon',51,'ICU-17','N02',.63,.09,103,94,38.2,100,23,.84,'Temperature rising'),
('P012','Adil Khan',66,'ICU-18','N02',.34,.02,88,96,37.4,115,19,.89,'Low-level trend'),
('P013','Priya Das',58,'ICU-19','N02',.78,.16,112,92,38.7,94,25,.86,'Oxygen and HR change'),
('P014','Joseph Mathew',73,'ICU-20','N02',.54,.06,98,95,37.8,108,21,.80,'Trend changed'),
('P015','Anika Roy',39,'ICU-21','N02',.22,-.02,75,99,36.7,124,15,.97,'Stable trend'),
('P016','Karthik Rao',64,'ICU-22','N02',.84,.19,116,91,38.9,90,28,.82,'Multi-signal deterioration'),
('P017','Fatima Ali',45,'ICU-23','N02',.46,.03,92,97,37.3,112,20,.91,'Mild change'),
('P018','Manu George',69,'ICU-24','N02',.71,.12,108,93,38.4,97,24,.84,'Rising risk'),
('P019','Sneha Paul',57,'ICU-25','N02',.31,.01,86,97,37.2,118,18,.92,'Stable monitoring'),
('P020','Vivek Kumar',61,'ICU-26','N02',.59,.07,100,95,38.0,104,22,.83,'Risk trend'),
('P021','Neha Sharma',52,'WARD-12','N03',.74,.14,111,93,38.3,98,25,.86,'Rising heart rate'),
('P022','Rohan Iyer',48,'WARD-13','N03',.27,-.01,81,98,37.0,120,17,.95,'Stable trend'),
('P023','Lakshmi Nair',70,'WARD-14','N03',.88,.23,119,90,39.1,87,30,.81,'Multi-signal deterioration'),
('P024','Dev Patel',33,'WARD-15','N03',.43,.04,95,97,37.6,111,20,.90,'Mild change'),
('P025','Maya Joseph',60,'WARD-16','N03',.61,.10,104,94,38.1,101,23,.85,'Oxygen trend'),
('P026','Harish Das',67,'WARD-17','N03',.36,.02,89,96,37.5,114,19,.89,'Low-level trend'),
('P027','Tara Singh',41,'WARD-18','N03',.19,-.02,76,99,36.8,123,16,.97,'Stable trend'),
('P028','Sanjay Rao',74,'WARD-19','N03',.82,.18,115,92,38.8,91,27,.83,'Risk accelerating'),
('P029','Aisha Thomas',37,'WARD-20','N03',.52,.06,99,95,37.9,107,22,.87,'Trend changed'),
('P030','Naveen Kumar',55,'WARD-21','N03',.69,.11,106,94,38.2,100,24,.85,'Rising risk'),
]
PATIENTS=[]
for x in names:
    p=dict(zip(['id','name','age','room','nurse','risk','velocity','hr','spo2','temp','sbp','resp','confidence','reason'],x))
    p['state']='High Risk' if p['risk']>=.8 else 'Elevated Risk' if p['risk']>=.6 else 'Monitoring' if p['risk']>=.35 else 'Stable'
    p['doctor']=next(n['doctor'] for n in NURSES if n['id']==p['nurse'])
    PATIENTS.append(p)


def get_db():
    DB.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB)


def init_db():
    con=get_db()
    con.executescript('''
    CREATE TABLE IF NOT EXISTS audit(
      id INTEGER PRIMARY KEY AUTOINCREMENT, actor TEXT, patient_id TEXT,
      action TEXT, details TEXT, ts TEXT
    );
    CREATE TABLE IF NOT EXISTS patient_assignments(
      patient_id TEXT PRIMARY KEY, nurse_id TEXT, doctor_id TEXT
    );
    CREATE TABLE IF NOT EXISTS monitoring_history(
      id INTEGER PRIMARY KEY AUTOINCREMENT, patient_id TEXT, source TEXT,
      hour INTEGER, hr REAL, spo2 REAL, temp REAL, sbp REAL, resp REAL,
      risk REAL, confidence REAL, ts TEXT
    );
    ''')
    for p in PATIENTS:
        con.execute('INSERT OR REPLACE INTO patient_assignments VALUES(?,?,?)',(p['id'],p['nurse'],p['doctor']))
    con.commit(); con.close()

init_db()


def data_files():
    return sorted(set(glob.glob(str(DATA/'*.psv')) + glob.glob(str(DATA/'**'/'*.psv'), recursive=True)))


def audit(actor, patient_id, action, details=''):
    con=get_db()
    con.execute('INSERT INTO audit(actor,patient_id,action,details,ts) VALUES(?,?,?,?,?)',(actor,patient_id,action,details,datetime.now().isoformat(timespec='seconds')))
    con.commit(); con.close()


def audit_rows(limit=50):
    con=get_db(); rows=con.execute('SELECT actor,patient_id,action,details,ts FROM audit ORDER BY id DESC LIMIT ?', (limit,)).fetchall(); con.close()
    keys=['actor','patient_id','action','details','ts']
    return [dict(zip(keys,r)) for r in rows]


def clean_num(v):
    try:
        x=float(v)
        return None if x != x else x
    except Exception:
        return None

@app.route('/')
def home():
    return send_from_directory(DASHBOARD,'index.html')

@app.route('/<path:path>')
def frontend(path):
    target=DASHBOARD/path
    if target.exists() and target.is_file():
        return send_from_directory(DASHBOARD,path)
    return send_from_directory(DASHBOARD,'index.html')

@app.get('/api/health')
def health():
    return jsonify({'ok':True,'dataset_files':len(data_files())})

@app.get('/api/state')
def state():
    return jsonify({'doctors':DOCTORS,'nurses':NURSES,'patients':PATIENTS,'dataset':{'files':len(data_files()),'target':200,'path':'data/physionet_2019'},'audit':audit_rows()})

@app.get('/api/doctor/<doctor_id>')
def doctor_view(doctor_id):
    d=next((x for x in DOCTORS if x['id']==doctor_id),None)
    if not d: return jsonify({'error':'Doctor not found'}),404
    nurses=[n for n in NURSES if n['id'] in d['nurses']]
    patients=[p for p in PATIENTS if p['doctor']==doctor_id]
    return jsonify({'doctor':d,'nurses':nurses,'patients':patients})

@app.get('/api/nurse/<nurse_id>')
def nurse_view(nurse_id):
    n=next((x for x in NURSES if x['id']==nurse_id),None)
    if not n: return jsonify({'error':'Nurse not found'}),404
    patients=[p for p in PATIENTS if p['nurse']==nurse_id]
    return jsonify({'nurse':n,'doctor':next(d for d in DOCTORS if d['id']==n['doctor']),'patients':patients})

@app.get('/api/patient/<patient_id>')
def patient_view(patient_id):
    p=next((x for x in PATIENTS if x['id']==patient_id),None)
    if not p: return jsonify({'error':'Patient not found'}),404
    nurse=next(n for n in NURSES if n['id']==p['nurse'])
    doctor=next(d for d in DOCTORS if d['id']==p['doctor'])
    return jsonify({'patient':p,'nurse':nurse,'doctor':doctor})

@app.post('/api/action')
def action():
    d=request.get_json(silent=True) or {}
    actor=d.get('actor','Demo User'); pid=d.get('patient_id',''); act=d.get('action','Clinical action'); details=d.get('details','')
    audit(actor,pid,act,details)
    return jsonify({'ok':True,'audit':audit_rows()})

@app.post('/api/replay')
def replay():
    d=request.get_json(silent=True) or {}; pid=d.get('patient_id','P001')
    p=next((x for x in PATIENTS if x['id']==pid),None)
    if not p: return jsonify({'error':'Patient not found'}),404
    delta=random.choice([.02,.03,.05,-.01])
    p['risk']=round(max(.05,min(.98,p['risk']+delta)),2)
    p['velocity']=round(max(-.05,p['velocity']+delta/2),2)
    p['hr']=max(60,p['hr']+random.choice([-2,1,3,5]))
    p['spo2']=max(88,min(99,p['spo2']+random.choice([-1,0,0,1])))
    p['temp']=round(p['temp']+random.choice([-.1,0,.1]),1)
    p['state']='High Risk' if p['risk']>=.8 else 'Elevated Risk' if p['risk']>=.6 else 'Monitoring' if p['risk']>=.35 else 'Stable'
    p['confidence']=round(max(.55,min(.99,p['confidence']+random.choice([-.02,0,.01]))),2)
    audit('Wearable Replay',pid,'Monitoring data received',f"Risk={p['risk']:.2f}; HR={p['hr']}; SpO2={p['spo2']}")
    con=get_db(); con.execute('INSERT INTO monitoring_history(patient_id,source,hour,hr,spo2,temp,sbp,resp,risk,confidence,ts) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(pid,'Simulated wearable',0,p['hr'],p['spo2'],p['temp'],p['sbp'],p['resp'],p['risk'],p['confidence'],datetime.now().isoformat(timespec='seconds'))); con.commit(); con.close()
    return jsonify(p)

@app.post('/api/assign')
def assign():
    d=request.get_json(silent=True) or {}; pid=d.get('patient_id'); nurse_id=d.get('nurse_id')
    p=next((x for x in PATIENTS if x['id']==pid),None); n=next((x for x in NURSES if x['id']==nurse_id),None)
    if not p or not n: return jsonify({'error':'Invalid patient or nurse'}),400
    p['nurse']=nurse_id; p['doctor']=n['doctor']
    con=get_db(); con.execute('INSERT OR REPLACE INTO patient_assignments VALUES(?,?,?)',(pid,nurse_id,n['doctor'])); con.commit(); con.close()
    audit('Doctor',pid,'Patient assigned',f"Assigned to {n['name']} under {n['doctor']}")
    return jsonify({'ok':True,'patient':p})

@app.get('/api/dataset')
def dataset():
    fs=data_files(); sample=[]
    for f in fs[:200]:
        try:
            with open(f,encoding='utf-8') as h:
                rows=list(csv.DictReader(h,delimiter='|'))
            labels=[int(float((r.get('SepsisLabel') or 0))) for r in rows]
            sample.append({'file':Path(f).name,'hours':len(rows),'sepsis_label_present':bool(max(labels) if labels else 0),'source':str(Path(f).relative_to(ROOT))})
        except Exception as e:
            sample.append({'file':Path(f).name,'hours':0,'sepsis_label_present':False,'source':str(Path(f).relative_to(ROOT)),'error':str(e)})
    return jsonify({'count':len(fs),'target':200,'sample':sample})

@app.get('/api/dataset/patient/<path:name>')
def dataset_patient(name):
    path=next((f for f in data_files() if Path(f).name==name),None)
    if not path: return jsonify({'error':'Patient file not found'}),404
    with open(path,encoding='utf-8') as h:
        rows=list(csv.DictReader(h,delimiter='|'))
    wanted=['HR','O2Sat','Temp','SBP','Resp','Lactate','WBC','ICULOS','SepsisLabel']
    out=[]
    for i,row in enumerate(rows):
        out.append({'hour':i, **{k:clean_num(row.get(k)) for k in wanted}})
    return jsonify({'file':name,'hours':len(out),'rows':out})

@app.post('/api/dataset/replay')
def dataset_replay():
    d=request.get_json(silent=True) or {}; name=d.get('file',''); hour=int(d.get('hour',0))
    path=next((f for f in data_files() if Path(f).name==name),None)
    if not path: return jsonify({'error':'Dataset file not found'}),404
    with open(path,encoding='utf-8') as h: rows=list(csv.DictReader(h,delimiter='|'))
    if not rows: return jsonify({'error':'Empty patient file'}),400
    hour=max(0,min(hour,len(rows)-1)); row=rows[hour]
    values={k:clean_num(row.get(k)) for k in ['HR','O2Sat','Temp','SBP','Resp','Lactate','WBC','ICULOS','SepsisLabel']}
    pid=d.get('patient_id','P001'); p=next((x for x in PATIENTS if x['id']==pid),PATIENTS[0])
    # Prototype risk mapping: transparent demonstration layer, not a clinical model.
    score=0.20
    if values['HR'] is not None and values['HR']>100: score+=0.15
    if values['O2Sat'] is not None and values['O2Sat']<94: score+=0.20
    if values['Temp'] is not None and values['Temp']>38: score+=0.15
    if values['Resp'] is not None and values['Resp']>22: score+=0.15
    if values['SBP'] is not None and values['SBP']<100: score+=0.10
    if values['Lactate'] is not None and values['Lactate']>2: score+=0.10
    score=round(min(.98,score),2)
    p['risk']=score; p['velocity']=round(score-p.get('_previous_replay_risk',score),2); p['_previous_replay_risk']=score
    if values['HR'] is not None: p['hr']=round(values['HR'])
    if values['O2Sat'] is not None: p['spo2']=round(values['O2Sat'])
    if values['Temp'] is not None: p['temp']=round(values['Temp'],1)
    if values['SBP'] is not None: p['sbp']=round(values['SBP'])
    if values['Resp'] is not None: p['resp']=round(values['Resp'])
    p['state']='High Risk' if score>=.8 else 'Elevated Risk' if score>=.6 else 'Monitoring' if score>=.35 else 'Stable'
    p['confidence']=round(.95 - min(.35, sum(v is None for v in values.values())*.05),2)
    reason=[]
    if values['O2Sat'] is not None and values['O2Sat']<94: reason.append('low SpO2')
    if values['HR'] is not None and values['HR']>100: reason.append('elevated HR')
    if values['Temp'] is not None and values['Temp']>38: reason.append('temperature')
    if values['Resp'] is not None and values['Resp']>22: reason.append('respiratory rate')
    if values['SBP'] is not None and values['SBP']<100: reason.append('low SBP')
    p['reason']=', '.join(reason) if reason else 'No threshold changes detected'
    audit('PhysioNet Replay',pid,'PhysioNet hour replayed',f"{name} | hour {hour} | SepsisLabel={values['SepsisLabel']}")
    con=get_db(); con.execute('INSERT INTO monitoring_history(patient_id,source,hour,hr,spo2,temp,sbp,resp,risk,confidence,ts) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(pid,'PhysioNet 2019',hour,p['hr'],p['spo2'],p['temp'],p['sbp'],p['resp'],p['risk'],p['confidence'],datetime.now().isoformat(timespec='seconds'))); con.commit(); con.close()
    return jsonify({'patient':p,'hour':hour,'total_hours':len(rows),'source_file':name,'raw':values})

if __name__ == '__main__':
    print('='*60)
    print('SepsisWatch+ running at http://127.0.0.1:5000/')
    print(f'PhysioNet files detected: {len(data_files())}')
    print('='*60)
    app.run(host='127.0.0.1',port=5000,debug=False)
