import streamlit as st
import calendar
import json
import os
from datetime import datetime

# --- 1. Configuration and Setup ---

# Set the layout of the web page to be wide
st.set_page_config(layout="wide", page_title="Dynamic To-Do Calendar")

# The file where tasks will be stored
DATA_FILE = "tasks.json"

# --- 2. Helper Functions for Loading/Saving Tasks ---

def load_tasks():
    """Loads tasks from the JSON file. Returns an empty dict if file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        # Return an empty dict if the file is empty
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_tasks(tasks):
    """Saves the tasks dictionary to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# --- 3. Initialize Session State ---

# Load tasks into the session state once, so it persists across reruns
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- 4. Sidebar for Controls and Adding Tasks ---

st.sidebar.header("🗓️ Calendar Controls")

# Get current date for default values
today = datetime.now()

# Dropdown to select the month
# The `index` is set to the current month - 1
selected_month_name = st.sidebar.selectbox(
    "Month",
    list(calendar.month_name)[1:],
    index=today.month - 1
)
# Convert month name to month number
selected_month = list(calendar.month_name).index(selected_month_name)

# Number input to select the year
selected_year = st.sidebar.number_input("Year", value=today.year, min_value=1900, max_value=2100)

st.sidebar.markdown("---")
st.sidebar.header("📝 Add a New Task")

# Form for adding a new task
with st.sidebar.form("add_task_form", clear_on_submit=True):
    task_date = st.date_input("Date for the task")
    task_desc = st.text_input("Task description")
    submit_button = st.form_submit_button("Add Task")

    if submit_button and task_desc:
        date_str = task_date.strftime("%Y-%m-%d")
        if date_str not in st.session_state.tasks:
            st.session_state.tasks[date_str] = []
        
        st.session_state.tasks[date_str].append({'task': task_desc, 'done': False})
        save_tasks(st.session_state.tasks)
        st.sidebar.success(f"Task added for {date_str}!")

# --- 5. Main Calendar Display ---

# Main title of the app
st.title(f"{selected_month_name} {selected_year}")

# Get the calendar matrix for the selected month and year
month_calendar = calendar.monthcalendar(selected_year, selected_month)

# Create 7 columns for the days of the week
cols = st.columns(7)
for i, day_name in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
    with cols[i]:
        st.markdown(f"**{day_name}**") # Make day names bold

st.markdown("---")

# Loop through each week in the month
for week in month_calendar:
    cols = st.columns(7)
    # Loop through each day in the week
    for i, day in enumerate(week):
        with cols[i]:
            # If the day is 0, it's an empty cell from another month
            if day == 0:
                st.write("")
            else:
                date_str = f"{selected_year}-{selected_month:02d}-{day:02d}"
                
                # Make today's date stand out
                if date_str == today.strftime("%Y-%m-%d"):
                    st.markdown(f"<p style='color: white; background-color: #FF4B4B; padding: 5px; border-radius: 5px; text-align: center;'><b>{day}</b></p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'><b>{day}</b></p>", unsafe_allow_html=True)
                
                # Display tasks for the current day
                if date_str in st.session_state.tasks:
                    for j, task in enumerate(st.session_state.tasks[date_str]):
                        # Each checkbox needs a unique key
                        unique_key = f"task_{date_str}_{j}"
                        
                        # `st.checkbox` returns True if checked, False otherwise
                        is_done = st.checkbox(
                            label=task['task'], 
                            value=task['done'], 
                            key=unique_key
                        )
                        
                        # If the checkbox state has changed, update the task and save
                        if is_done != task['done']:
                            st.session_state.tasks[date_str][j]['done'] = is_done
                            save_tasks(st.session_state.tasks)
                            st.experimental_rerun() # Rerun to reflect the change instantly