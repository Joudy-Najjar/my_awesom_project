import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    
    # إنشاء ID فريد للمهمة الجديدة (إذا كانت القائمة فارغة يبدأ من 1)
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    
    now = datetime.now().isoformat()
    
    new_task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_tracker.py <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Please provide a task description.")
        else:
            description = sys.argv[2]
            add_task(description)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()