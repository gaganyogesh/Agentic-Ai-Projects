# AI-Based Interactive Storytelling Agent (M1-P8)

A Streamlit application for interactive, evolving stories. The user supplies a theme, setting and characters, then makes decisions that influence later chapters. The agent stores story memory in JSON so characters, events and choices remain available across chapters and app restarts.

## Features
- Start a story from a theme, setting and character list.
- Generate subsequent chapters based on user decisions.
- Preserve character names, prior events and previous choices.
- View the agent's story memory.
- Save the current story state locally and download it as JSON.
- Works offline with a built-in narrative engine.
- Optional OpenAI API integration for more flexible language generation.

## Requirements
- Python 3.9+
- Streamlit
- Optional: `openai` Python package and an API key for LLM mode.

## Run offline
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

## Enable optional LLM mode
Install the optional package:
```bash
pip install openai
```
Set your API key as an environment variable (do not paste it into source code):
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your-api-key"
# macOS/Linux
export OPENAI_API_KEY="your-api-key"
```
Optional model override:
```bash
# Windows PowerShell
$env:OPENAI_MODEL="gpt-4o-mini"
# macOS/Linux
export OPENAI_MODEL="gpt-4o-mini"
```
Then run `streamlit run app.py`. If the API is unavailable or the key is not set, the app uses its offline engine.

## Project structure
```text
interactive_storytelling_agent/
├── app.py
├── requirements.txt
├── README.md
└── data/                 # created automatically; stores story_state.json
```

## Agent workflow
1. Receive the theme, setting and character names.
2. Generate the opening chapter.
3. Receive a user decision.
4. Retrieve stored characters, events and decisions.
5. Generate the next chapter using the story context.
6. Save the new chapter and update the agent's memory.

## Limitations and future enhancements
Offline generation is rule-based and offers a limited set of branching patterns. Optional LLM mode improves narrative variety but requires an API key and may incur usage charges. Future enhancements include character profiles, plot graphs, user-defined genres, chapter editing and export to PDF.
