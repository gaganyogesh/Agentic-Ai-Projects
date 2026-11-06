# AI Agent Mini Projects: M1-P7 and M1-P8

This package contains two independent Python + Streamlit projects:

1. `event_planning_agent` — Autonomous Event Planning Agent (M1-P7)
2. `interactive_storytelling_agent` — AI-Based Interactive Storytelling Agent (M1-P8)

## Quick start
Open a terminal in either project folder, create a virtual environment, install its requirements and run:
```bash
pip install -r requirements.txt
streamlit run app.py
```
Each app runs independently. See the individual README files for detailed instructions.

Both projects store their state in their own `data/` folder. The event planner uses local task templates and progress tracking. The storytelling app works offline and optionally supports OpenAI-powered generation when configured with an API key.
