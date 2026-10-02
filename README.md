# SepsisWatch+

### AI-Assisted Clinical Decision Support for Early Sepsis Risk Monitoring

**Hackathon Project | AI in Healthcare**

SepsisWatch+ is an AI-assisted healthcare prototype designed to support continuous monitoring of patients at risk of clinical deterioration and sepsis.

The system combines physiological data, risk trajectory analysis, explainable risk factors, data-confidence assessment, intelligent patient prioritization, and clinician-in-the-loop review into a role-based healthcare monitoring platform.

> **Important:** SepsisWatch+ is a research and hackathon prototype. It is not intended to replace doctors, nurses, or clinical decision-making.

---

## 🏥 Problem

Sepsis and patient deterioration can develop rapidly, while healthcare teams may need to monitor many patients simultaneously.

A monitoring system should therefore do more than display individual vital signs.

It should help answer:

* Is the patient's risk increasing?
* How quickly is the risk changing?
* What physiological factors contributed to the change?
* How reliable or complete is the available data?
* Which patient requires attention first?
* Which nurse is responsible for the patient?
* Which doctor supervises the nursing team?
* What happened after an alert was generated?

SepsisWatch+ was designed around these questions.

---

## 💡 Proposed Solution

SepsisWatch+ creates a connected monitoring workflow:

```text
PhysioNet Patient Data
        │
        ▼
Data & Replay Lab
        │
        ▼
Patient Monitoring
        │
        ▼
Risk & Trajectory Analysis
        │
        ├── Risk Level
        ├── Deterioration Velocity
        ├── Explainable Factors
        └── Data Confidence
        │
        ▼
Smart Patient Prioritization
        │
        ├── Nurse Portal
        │
        └── Doctor Portal
                 │
                 ▼
          Clinician Review
                 │
                 ▼
             Audit Trail
```

A simulated wearable stream is also included to demonstrate how continuous patient monitoring could connect a wearable device to the patient application and clinical monitoring workflow.

---

# 👨‍⚕️ Doctor Portal

The doctor portal is designed around **clinical supervision rather than simply viewing all patients**.

Each doctor has an independent clinical team.

Example:

```text
Dr. Ananya Rao
│
├── Nurse Meera
│   ├── Patient 01
│   ├── Patient 02
│   └── ...
│
└── Nurse Kavya
    ├── Patient 11
    ├── Patient 12
    └── ...
```

A doctor can:

* View assigned nursing teams
* View patients under each nurse
* Monitor patient risk
* Examine deterioration trends
* View physiological measurements
* Review risk explanations
* Check data confidence
* Review patient priorities
* Assign/reassign patients to nurses
* Review nurse activity
* Perform clinician review actions
* Inspect the clinical audit trail

The doctor therefore sees the **hierarchy of doctor → nurses → patients**.

---

# 👩‍⚕️ Nurse Portal

The nurse portal focuses on **continuous patient monitoring and prioritization**.

Each nurse is assigned a defined group of patients.

Example:

```text
Nurse Meera
│
├── Patient 01
├── Patient 02
├── Patient 03
├── ...
└── Patient 10
```

The nurse can:

* Monitor assigned patients
* View current vital signs
* View risk levels
* View patient priority
* Monitor deterioration velocity
* View alert explanations
* Check data confidence
* Receive new monitoring data
* Acknowledge alerts
* Record monitoring/review actions
* View the supervising doctor
* Review the audit history

The portal is designed around the practical question:

> **Which of my patients needs attention right now, and why?**

---

# 🧑‍🦽 Patient Portal

The patient interface is intentionally different from the clinical portals.

The patient receives information through two connected layers.

### 1. Wearable

A simulated smart-band interface represents continuous physiological monitoring.

```text
Smart Band
    │
    ├── Heart Rate
    ├── SpO₂
    ├── Temperature
    └── Monitoring Status
```

### 2. Patient Application

The patient's desktop/application interface provides a simplified view of their own monitoring information.

```text
Wearable
   ↓
Patient Application
   ↓
Monitoring API
   ↓
Clinical System
   ↓
Assigned Nurse
   ↓
Supervising Doctor
```

The patient does **not** receive the same clinical information available to doctors and nurses.

This demonstrates role-based access and patient-oriented presentation.

---

# 🧪 PhysioNet Data & Replay Lab

The project uses real physiological records from the **PhysioNet Challenge 2019 dataset**.

For the hackathon prototype, a subset of 200 patient `.psv` files is used.

The Data & Replay Lab allows the dataset to become part of the actual demonstration instead of being hidden somewhere inside the project folder.

The lab can:

* Detect available PhysioNet records
* Display individual patient files
* Inspect hourly physiological measurements
* View sepsis labels
* Select patient records
* Replay physiological observations
* Feed observations into the monitoring workflow
* Update the monitoring interface
* Record replay activity in the audit trail

Relevant measurements include:

* Heart rate
* Oxygen saturation
* Temperature
* Systolic blood pressure
* Respiratory rate
* Lactate
* WBC
* ICU length of stay
* Sepsis label

---

# 🧠 AI-Assisted Risk Monitoring

The system is designed around multiple signals rather than a single static risk value.

### Risk Level

Represents the current estimated level of concern.

### Risk Trajectory

Tracks how the patient's risk changes over time.

```text
Risk
 │
 │          ╭───
 │       ╭──╯
 │    ╭──╯
 │ ╭──╯
 └──────────────── Time
```

### Deterioration Velocity

Measures the direction and rate of risk change.

A patient whose risk is rapidly increasing can therefore be distinguished from a patient whose risk is relatively stable.

### Explainable Factors

The system provides contributing physiological factors to support clinician interpretation.

### Data Confidence

The system considers the availability and quality of monitoring data.

This is important because an apparent change in patient condition should be interpreted differently when the underlying measurements are incomplete or unreliable.

---

# 🚨 Smart Patient Prioritization

Instead of presenting patients as an undifferentiated list, the system creates a monitoring priority based on factors such as:

```text
Current Risk
      +
Risk Trajectory
      +
Deterioration Velocity
      +
Data Confidence
      +
Clinical Signals
      ↓
Patient Priority
```

This allows nurses to focus attention on patients showing meaningful changes.

The priority system is intended as **decision support**, not an autonomous clinical decision-maker.

---

# 👨‍⚕️ Human-in-the-Loop Design

SepsisWatch+ does not automatically prescribe treatment.

The intended workflow is:

```text
AI detects increased risk
        ↓
Alert / Priority generated
        ↓
Nurse reviews patient
        ↓
Doctor can review the case
        ↓
Clinician makes the clinical decision
```

This keeps the system focused on **clinical decision support** rather than replacing healthcare professionals.

---

# 📋 Clinical Audit Trail

Important system actions are recorded in an audit trail.

Examples include:

* Monitoring data received
* Alert generated
* Alert acknowledged
* Patient assignment changed
* Clinical review performed
* Dataset replay executed

This provides traceability during demonstrations and supports future research into accountable AI-assisted healthcare systems.

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │   PhysioNet Data    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Data & Replay Lab   │
                    └──────────┬──────────┘
                               │
                               ▼
┌──────────────┐      ┌─────────────────────┐      ┌──────────────┐
│ Smart Band   │ ───► │   Flask Backend     │ ◄─── │ Patient App  │
└──────────────┘      └──────────┬──────────┘      └──────────────┘
                                  │
                                  ▼
                         ┌────────────────┐
                         │ Risk Engine    │
                         └───────┬────────┘
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
          Risk/TREND       Explainability    Confidence
                │                │                │
                └────────────────┼────────────────┘
                                 ▼
                       ┌────────────────────┐
                       │ Priority Engine    │
                       └─────────┬──────────┘
                                 │
                       ┌─────────┴─────────┐
                       ▼                   ▼
                Nurse Portal        Doctor Portal
                       │                   │
                       └─────────┬─────────┘
                                 ▼
                         Clinical Audit
```

---

# 🛠️ Technology Stack

### Backend

* Python
* Flask
* SQLite
* REST API

### Frontend

* HTML
* CSS
* JavaScript

### AI / Data Science

* Physiological time-series analysis
* Risk trajectory analysis
* Explainable risk factors
* Data-confidence assessment
* Patient prioritization

### Dataset

* PhysioNet Challenge 2019
* 200 patient records used for the hackathon prototype

### Development

* Visual Studio Code
* Git
* GitHub

---

# 📂 Project Structure

```text
sepsiswatch/
│
├── backend/
│   └── app.py
│
├── dashboard/
│   ├── index.html
│   ├── clinical.html
│   └── patient.html
│
├── data/
│   └── physionet_2019/
│
├── docs/
│   ├── DATA_SOURCES.md
│   └── NOVELTY_AND_PAPER.md
│
├── scripts/
│   ├── check_data.py
│   └── download_physionet_200.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Running the Project

Create and activate the virtual environment:

```bash
python -m venv .venv
```

Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Place the downloaded PhysioNet `.psv` files inside:

```text
data/physionet_2019/
```

Check the dataset:

```bash
python scripts/check_data.py
```

Start the application:

```bash
python backend/app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

---

# 🔬 Research Direction

The prototype is designed as a foundation for further research into:

* Early deterioration detection
* Patient-specific risk trajectories
* Explainable clinical decision support
* Data-quality-aware AI
* Intelligent clinical prioritization
* Human-in-the-loop healthcare AI
* Continuous wearable-assisted monitoring
* Clinical auditability

Future evaluation can compare the proposed monitoring workflow against conventional threshold-based alerting using metrics such as alert burden, detection lead time, false-alert rate, and prioritization consistency.

---

# ⚠️ Disclaimer

SepsisWatch+ is an academic/hackathon prototype created for research and demonstration purposes.

It is **not a medical device** and must not be used to diagnose, treat, or make clinical decisions for real patients.

All wearable measurements shown in the prototype are simulated unless explicitly identified as dataset-derived.

---

## 👩‍💻 Project

**SepsisWatch+**

**Theme:** AI in Healthcare
**Purpose:** Hackathon / Research Prototype
**Focus:** AI-assisted continuous patient deterioration and sepsis-risk monitoring

