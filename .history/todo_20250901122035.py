import calendar
import json
import os
from datetime import datetime

# The file where tasks will be stored
DATA_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    """Saves tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def display_calendar(year, month, tasks):
    """Displays the calendar for a given month and lists its tasks."""
    cal = calendar.TextCalendar(calendar.SUNDAY)
    month_calendar = cal.formatmonth(year, month)

    print("\n" + month_calendar)
    print("-" * 25)
    print("Tasks for this month:")

    has_tasks = False
    # Sort dates for chronological order
    sorted_dates = sorted(tasks.keys())

    for date_str in sorted_dates:
        try:
            task_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            if task_date.year == year and task_date.month == month:
                has_tasks = True
                print(f"\n--- {date_str} ---")
                for i, task in enumerate(tasks[date_str]):
                    status = "✅" if task['done'] else "🔲"
                    print(f"  {i + 1}. {status} {task['task']}")
        except ValueError:
            continue # Skip invalid date strings if any

    if not has_tasks:
        print("  No tasks for this month.")
    print("-" * 25)


def add_task(tasks):
    """Adds a new task to the list."""
    try:
        date_str = input("Enter date (YYYY-MM-DD): ")
        # Validate date format
        datetime.strptime(date_str, "%Y-%m-%d")
        
        task_description = input("Enter task description: ")
        
        if date_str not in tasks:
            tasks[date_str] = []
            
        tasks[date_str].append({'task': task_description, 'done': False})
        save_tasks(tasks)
        print("✅ Task added successfully!")
    except ValueError:
        print("❌ Invalid date format. Please use YYYY-MM-DD.")

def toggle_task_status(tasks):
    """Marks a task as complete or incomplete."""
    try:
        date_str = input("Enter date of the task (YYYY-MM-DD): ")
        if date_str not in tasks or not tasks[date_str]:
            print("No tasks found for this date.")
            return

        print(f"\nTasks for {date_str}:")
        for i, task in enumerate(tasks[date_str]):
            status = "✅" if task['done'] else "🔲"
            print(f"  {i + 1}. {status} {task['task']}")
        
        task_num = int(input("Enter the task number to toggle: "))
        if 1 <= task_num <= len(tasks[date_str]):
            tasks[date_str][task_num - 1]['done'] = not tasks[date_str][task_num - 1]['done']
            save_tasks(tasks)
            print("🔄 Task status updated!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
    except KeyError:
        print("❌ No tasks found for the specified date.")


def main():
    """Main function to run the application loop."""
    tasks = load_tasks()
    
    while True:
        print("\n--- Python Calendar App ---")
        print("1. View Calendar & Tasks")
        print("2. Add Task")
        print("3. Update Task Status")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            try:
                year = int(input("Enter year (e.g., 2025): "))
                month = int(input("Enter month (1-12): "))
                if 1 <= month <= 12:
                    display_calendar(year, month, tasks)
                else:
                    print("❌ Invalid month. Please enter a number between 1 and 12.")
            except ValueError:
                print("❌ Invalid input. Please enter numbers for year and month.")
        
        elif choice == '2':
            add_task(tasks)
        
        elif choice == '3':
            toggle_task_status(tasks)
            
        elif choice == '4':
            print("Goodbye!")
            break
            
        else:
            print("❌ Invalid option. Please choose again.")

if __name__ == "__main__":
    main()