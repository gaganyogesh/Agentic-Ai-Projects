# Autonomous Event Planning Agent (M1-P7)

A Streamlit application that converts a high-level event requirement into a structured checklist of planning activities. It tracks task status, owners and due dates, identifies unfinished work, and stores the plan locally.

## Features
- Generate a plan for a technical workshop or another event.
- Break the plan into objectives, budget, venue, schedule, resources, publicity, registration, communication, operations and follow-up.
- Track each task as Not started, In progress, Completed or Blocked.
- Assign owners and due dates.
- View all unfinished activities and download the plan as JSON.
- Persist the latest plan in `data/event_plan.json`.

## Requirements
- Python 3.9+
- Streamlit

## Run
```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL printed by Streamlit (usually http://localhost:8501).

## Project structure
```text
event_planning_agent/
├── app.py
├── requirements.txt
├── README.md
└── data/                 # created automatically; stores event_plan.json
```

## Agent workflow
1. Receive the event brief and basic event details.
2. Decompose the brief into planning tasks.
3. Save the plan and its task state.
4. Let the organizer update progress, owners and due dates.
5. Identify every activity whose status is not Completed.

## Limitations and future enhancements
This academic prototype uses a transparent task template rather than an external language model. Real-world booking, payments, email and calendar actions require integrations and explicit approval. Future work can add dependency-aware scheduling, risk estimation, LLM-based task generation and calendar/email connectors.
