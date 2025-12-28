- Focus Drift

A privacy-first attention analysis tool built for understanding work patterns, not tracking behavior.

- Overview

Focus Drift is a Chrome extension + web dashboard that helps users understand how their attention moves during a work session.

Instead of tracking content or productivity, Focus Drift analyzes behavioral patterns such as:

Tab switching frequency

Context changes

Session stability

Attention fragmentation

The goal is awareness, not surveillance.
- Why Focus Drift?

Most productivity tools:

Track time

Judge output

Guess intent

Collect invasive data

Focus Drift takes a different approach:

We analyze how attention behaves, not what the user is doing.

This makes the system:

Privacy-safe

Explainable

Honest

Lightweight

- What the System Does
 1️) Chrome Extension

User manually starts and ends a session

Tracks only:

Tab switches

Tab creation/removal

Domain changes

Window focus

 No keystrokes

 No page content

 No background tracking

 2) Backend Processing

The backend computes:

Session duration

Tab switch rate

Rapid switching behavior

Time spent per domain

Attention stability

These metrics are deterministic (not AI-generated).

 3) AI Insight Layer

An LLM is used only to:

Interpret the computed metrics

Generate a short, human-readable summary

⚠️ The AI does not:

See browsing content

Analyze URLs

Guess user intent

 4) Streamlit Dashboard

Displays:

Session duration

Focus score

Session type

Domain usage

Insight summary

Designed to be:

Minimal

Readable

Non-judgmental

- Focus Score Explained

Focus Score is based on tab switching frequency.

Higher switching → Lower focus stability
Lower switching → Higher focus stability


Example:

1–2 switches/min → High focus

4–6 switches/min → Mixed attention

8+ switches/min → Fragmented attention

This makes the score:
✔ Transparent
✔ Explainable
✔ Behavior-based

- Session Classification
Type	Meaning
Focused Session	Stable attention, low switching
Mixed Attention	Moderate context switching
Fragmented Session	Frequent context shifts

- This is not a productivity judgment — only a behavioral description.

🛠 Tech Stack
Frontend

Chrome Extension (Manifest v3)

JavaScript

HTML / CSS

Backend

Python

FastAPI

AI Layer

OpenAI API

Used only for insight generation

Visualization

Streamlit

- Project Structure
.
├── hackx-extension/
│   ├── background.js
│   ├── popup.html
│   ├── popup.js
│   └── manifest.json
│
├── backend/
│   ├── api.py
│   ├── app.py
│   ├── process_session.py
│   ├── llm_analysis.py
│   └── latest_session.json
│
└── README.md

- How to Run
1. Start Backend
cd backend
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload

2. Start Streamlit Dashboard
streamlit run app.py

3. Load Chrome Extension

Open chrome://extensions

Enable Developer Mode

Click Load unpacked

Select the hackx-extension/ folder

4. Use the App

Click Start Session

Browse normally

Click End Session

View insights automatically in browser

- Privacy Philosophy

✔ No content tracking
✔ No keystrokes
✔ No background monitoring
✔ No user accounts
✔ Session-only analysis

Focus Drift analyzes behavior, not identity.

- Future Improvements

Session history & comparisons

Attention trends over time

Optional session labeling

Offline / local-only analysis

Visual timeline of attention shifts

- Team

Built as part of HackX
Focused on behavior-aware, privacy-first systems.

- Final Note

Focus Drift doesn’t tell you how to work.
It shows you how your attention actually behaves.