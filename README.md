# SepsisWatch+

A role-based clinical decision-support prototype for a hackathon/research demonstration.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python backend\app.py
```

Open `http://127.0.0.1:5000/`.

## Data

Put the 200 downloaded PhysioNet Challenge 2019 `.psv` files in `data/physionet_2019/`, or run:

```powershell
python scripts\download_physionet_200.py
```

Check them with:

```powershell
python scripts\check_data.py
```

Raw PhysioNet files stay outside SQLite. SQLite stores application state, assignments, monitoring history and audit events.

## Role model

- Doctor D01: Nurse N01 + N02, 20 patients total.
- Doctor D02: Nurse N03, 10 patients total.
- Each nurse has a 10-patient monitoring board.
- Patient view is separate from clinician views and is wearable-first.

## Data & Replay Lab

The lab lists detected real `.psv` files, exposes hourly rows, and can replay a selected real row through a transparent prototype risk-mapping layer. The result flows into a demo patient state and creates an audit event.

The replay risk mapping is explicitly a demonstration layer, not a validated clinical model.

## Prototype boundaries

The system is not a medical device and does not autonomously prescribe medication or treatment. Clinical actions remain clinician-controlled.
