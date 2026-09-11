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

def list_tasks(status_filter=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    filtered_tasks = tasks
    if status_filter:
        filtered_tasks = [t for t in tasks if t["status"] == status_filter]

    if not filtered_tasks:
        print(f"No tasks found with status: {status_filter}")
        return

    for task in filtered_tasks:
        print(f"[{task['id']}] {task['description']} - Status: {task['status']}")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t["id"] != task_id]
    
    if len(tasks) == len(updated_tasks):
        print(f"Error: Task with ID {task_id} not found.")
    else:
        save_tasks(updated_tasks)
        print(f"Task {task_id} deleted successfully.")

def change_status(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_tracker.py <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) >= 3:
        add_task(sys.argv[2])
    elif command == "list":
        status = sys.argv[2] if len(sys.argv) >= 3 else None
        list_tasks(status)
    elif command == "update" and len(sys.argv) >= 4:
        update_task(int(sys.argv[2]), sys.argv[3])
    elif command == "delete" and len(sys.argv) >= 3:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) >= 3:
        change_status(int(sys.argv[2]), "in-progress")
    elif command == "mark-done" and len(sys.argv) >= 3:
        change_status(int(sys.argv[2]), "done")
    else:
        print("Invalid command or missing arguments.")

if __name__ == "-_main__":
    main()