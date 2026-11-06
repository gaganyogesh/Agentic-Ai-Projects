import json
import os
from pathlib import Path
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
STATE_FILE = DATA_DIR / "story_state.json"

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

def local_story_segment(state, decision):
    """A lightweight offline narrative engine that preserves story continuity."""
    theme = state["theme"].strip()
    chapter = len(state["chapters"]) + 1
    characters = state["characters"]
    events = state["events"]
    hero = characters[0] if characters else "the traveler"
    companion = characters[1] if len(characters) > 1 else "a mysterious guide"
    place = state.get("setting") or "a forgotten place"
    choice = decision.lower()

    if chapter == 1:
        text = (f"## Chapter {chapter}: The First Sign\\n\\n"
                f"In a world shaped by **{theme}**, {hero} arrived at {place}. "
                f"An unusual signal appeared just before sunset. {companion} noticed it too, "
                f"and warned that the sign was connected to an old event no one wanted to remember. "
                f"Together, they had to decide what to do next.")
        new_event = f"{hero} discovered a mysterious signal at {place}."
    else:
        previous = events[-1] if events else "the journey began"
        if "investigate" in choice or "explore" in choice or "follow" in choice:
            text = (f"## Chapter {chapter}: Into the Unknown\\n\\n"
                    f"Following the previous discovery — {previous} — {hero} and {companion} "
                    f"chose to investigate. Their search led them deeper into {place}, where a hidden clue "
                    f"revealed that the mystery was larger than they imagined. A new ally offered help, "
                    f"but demanded a difficult promise in return.")
            new_event = f"The characters investigated the clue and found a possible ally."
        elif "talk" in choice or "help" in choice or "trust" in choice:
            text = (f"## Chapter {chapter}: An Uneasy Alliance\\n\\n"
                    f"Remembering {previous}, {hero} decided to seek help rather than act alone. "
                    f"{companion} opened a conversation with the stranger. Their exchange uncovered "
                    f"a forgotten connection between the characters and the mystery. Trust grew, "
                    f"but a secret remained hidden.")
            new_event = "The characters formed an uneasy alliance and uncovered a connection."
        elif "leave" in choice or "escape" in choice or "avoid" in choice:
            text = (f"## Chapter {chapter}: A Different Path\\n\\n"
                    f"After {previous}, {hero} chose to leave {place} and avoid the obvious danger. "
                    f"The decision kept the group safe for now, but the mystery followed them. "
                    f"On the road, they found evidence that someone had predicted this exact choice.")
            new_event = "The group left the location, but the mystery followed them."
        else:
            text = (f"## Chapter {chapter}: The Choice\\n\\n"
                    f"Building on {previous}, {hero} chose: **{decision}**. "
                    f"{companion} considered the consequences while a new clue changed their understanding "
                    f"of the {theme} mystery. The next step would test their courage and loyalty.")
            new_event = f"The group acted on the decision: {decision}."

    return text, new_event

def generate_segment(state, decision):
    # Optional OpenAI integration. The app works offline when no API key/package is configured.
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            prompt = (
                "Continue this interactive story in 2-4 engaging paragraphs. Maintain continuity. "
                "Do not contradict the established characters or events. Add a meaningful new event. "
                f"Theme: {state['theme']}. Setting: {state['setting']}. "
                f"Characters: {state['characters']}. Previous events: {state['events']}. "
                f"User decision: {decision}. Return only the next story chapter."
            )
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.85,
            )
            return response.choices[0].message.content, f"User decision: {decision}"
        except Exception as exc:
            st.warning(f"LLM request failed; using offline story engine instead. Details: {exc}")
    return local_story_segment(state, decision)

st.set_page_config(page_title="AI Interactive Storytelling Agent", page_icon="📖", layout="wide")
st.title("📖 AI-Based Interactive Storytelling Agent")
st.caption("Create an evolving story. Characters, events and your decisions are carried into later chapters.")

state = load_state()
with st.sidebar:
    st.header("Create a story")
    with st.form("story_setup"):
        theme = st.text_input("Theme", value="mystery and friendship")
        setting = st.text_input("Story setting", value="an abandoned observatory")
        character_text = st.text_input("Main characters (comma-separated)", value="Mira, Arin")
        start = st.form_submit_button("Start new story", type="primary")
    if start:
        characters = [x.strip() for x in character_text.split(",") if x.strip()]
        if not characters:
            characters = ["the traveler"]
        state = {"theme": theme, "setting": setting, "characters": characters,
                 "events": [], "chapters": [], "decisions": []}
        save_state(state)
        st.rerun()
    if state and st.button("Reset current story"):
        STATE_FILE.unlink(missing_ok=True)
        st.rerun()

if not state:
    st.info("Enter a theme and characters in the sidebar, then start your story.")
    st.markdown("**Continuity features:** the agent stores character names, story events, chapters and user decisions in a local JSON file.")
    st.stop()

st.subheader(f"Theme: {state['theme']}")
st.write(f"**Setting:** {state['setting']}  |  **Characters:** {', '.join(state['characters'])}")

for chapter in state["chapters"]:
    st.markdown(chapter["text"])
    st.caption(f"Decision: {chapter['decision']}")

st.divider()
st.subheader("What should happen next?")
decision = st.text_area("Your decision", placeholder="Example: Investigate the strange signal together.")
if st.button("Generate next chapter", type="primary", disabled=not decision.strip()):
    segment, event = generate_segment(state, decision.strip())
    state["chapters"].append({"text": segment, "decision": decision.strip()})
    state["decisions"].append(decision.strip())
    state["events"].append(event)
    save_state(state)
    st.rerun()

with st.expander("Story memory (agent state)"):
    st.markdown("**Characters**")
    st.write(", ".join(state["characters"]))
    st.markdown("**Events remembered**")
    for i, event in enumerate(state["events"], 1):
        st.write(f"{i}. {event}")
    st.markdown("**Decisions made**")
    for i, item in enumerate(state["decisions"], 1):
        st.write(f"{i}. {item}")
    st.download_button("Download story memory (JSON)", json.dumps(state, indent=2, ensure_ascii=False),
                       file_name="story_state.json", mime="application/json")

st.divider()
st.caption("Offline mode uses a lightweight rule-based narrative engine. For richer LLM-generated chapters, configure OPENAI_API_KEY and install the optional OpenAI package.")
