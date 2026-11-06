import json
from pathlib import Path
from datetime import date
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
PLAN_FILE = DATA_DIR / "event_plan.json"

TASK_TEMPLATES = [
    ("Define event objectives", "Confirm the purpose, audience, expected outcomes and success criteria.", "Planning"),
    ("Estimate budget", "List expected costs and allocate a budget for venue, food, equipment and promotion.", "Resources"),
    ("Identify venue requirements", "Choose a suitable venue or online platform, capacity, location and accessibility needs.", "Venue"),
    ("Prepare event schedule", "Create the agenda, session timings, breaks and speaker slots.", "Schedule"),
    ("Arrange speakers and resources", "Confirm speakers, volunteers, equipment, internet, presentation tools and materials.", "Resources"),
    ("Plan publicity", "Prepare posters, announcements, social posts and a registration announcement.", "Publicity"),
    ("Set up registration", "Create a registration form and define participant limits and registration deadlines.", "Participants"),
    ("Communicate with participants", "Send invitations, confirmations, joining instructions and reminders.", "Communication"),
    ("Prepare event-day checklist", "Assign responsibilities and verify venue, equipment, attendance and contingency plans.", "Operations"),
    ("Collect feedback and close event", "Share a feedback form, review outcomes and document lessons learned.", "Follow-up"),
]

def load_plan():
    if PLAN_FILE.exists():
        try:
            return json.loads(PLAN_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None

def save_plan(plan):
    PLAN_FILE.write_text(json.dumps(plan, indent=2), encoding="utf-8")

def create_plan(title, description, audience, event_date, attendees):
    tasks = []
    for i, (name, detail, category) in enumerate(TASK_TEMPLATES, 1):
        tasks.append({"id": i, "name": name, "detail": detail, "category": category,
                      "status": "Not started", "owner": "", "due_date": ""})
    return {
        "title": title, "description": description, "audience": audience,
        "event_date": str(event_date), "expected_attendees": attendees,
        "created_on": str(date.today()), "tasks": tasks
    }

st.set_page_config(page_title="Autonomous Event Planning Agent", page_icon="🗓️", layout="wide")
st.title("🗓️ Autonomous Event Planning Agent")
st.caption("Turn a high-level event idea into an actionable plan, track progress and find unfinished activities.")

plan = load_plan()
with st.sidebar:
    st.header("Create an event plan")
    with st.form("new_plan"):
        title = st.text_input("Event name", value="Technical Workshop")
        description = st.text_area("High-level requirement", value="Organize a technical workshop with sessions, speakers and participant interaction.")
        audience = st.text_input("Target audience", value="College students")
        event_date = st.date_input("Proposed event date")
        attendees = st.number_input("Expected participants", min_value=1, max_value=100000, value=100)
        submitted = st.form_submit_button("Generate plan", type="primary")
    if submitted:
        plan = create_plan(title, description, audience, event_date, int(attendees))
        save_plan(plan)
        st.success("Plan generated and saved.")
        st.rerun()
    if plan and st.button("Start a fresh plan"):
        PLAN_FILE.unlink(missing_ok=True)
        st.rerun()

if not plan:
    st.info("Create an event plan from the sidebar to begin.")
    st.markdown("**How it works:** The agent interprets the event brief, decomposes it into planning workstreams, saves task state locally and highlights unfinished activities.")
    st.stop()

st.subheader(plan["title"])
st.write(plan["description"])
c1, c2, c3 = st.columns(3)
c1.metric("Target participants", plan["expected_attendees"])
c2.metric("Event date", plan["event_date"])
done = sum(t["status"] == "Completed" for t in plan["tasks"])
c3.metric("Completed tasks", f'{done}/{len(plan["tasks"])}')
st.progress(done / len(plan["tasks"]))

tab1, tab2, tab3 = st.tabs(["Task board", "Unfinished activities", "Event brief"])
with tab1:
    st.write("Update each activity. Changes are saved automatically.")
    for task in plan["tasks"]:
        with st.expander(f'{task["id"]}. {task["name"]} — {task["status"]}', expanded=False):
            st.write(task["detail"])
            a, b, c = st.columns([1, 1, 1])
            statuses = ["Not started", "In progress", "Completed", "Blocked"]
            current = statuses.index(task["status"]) if task["status"] in statuses else 0
            task["status"] = a.selectbox("Status", statuses, index=current, key=f'status_{task["id"]}')
            task["owner"] = b.text_input("Owner", value=task.get("owner", ""), key=f'owner_{task["id"]}')
            task["due_date"] = c.text_input("Due date", value=task.get("due_date", ""), placeholder="YYYY-MM-DD", key=f'due_{task["id"]}')
    if st.button("Save all task updates", type="primary"):
        save_plan(plan)
        st.success("Task updates saved.")

with tab2:
    unfinished = [t for t in plan["tasks"] if t["status"] != "Completed"]
    if unfinished:
        st.warning(f"{len(unfinished)} activities are not yet complete.")
        for t in unfinished:
            st.markdown(f'- **{t["name"]}** — {t["status"]}. {t["detail"]}')
    else:
        st.success("All activities are completed.")

with tab3:
    st.write(f"**Audience:** {plan['audience']}")
    st.write(f"**Created on:** {plan['created_on']}")
    st.write(f"**Expected participants:** {plan['expected_attendees']}")
    st.download_button("Download plan as JSON", json.dumps(plan, indent=2), file_name="event_plan.json", mime="application/json")

st.divider()
st.caption("Prototype note: task decomposition uses an editable planning template and local JSON persistence. It does not book venues, send messages or make purchases automatically.")
