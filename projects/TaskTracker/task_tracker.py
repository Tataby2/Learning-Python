from enum import Enum
import json, time
import os
from datetime import datetime

# Define the path to the tasks JSON file
TASKS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

# Enum to represent task status
class Status(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

#region Task IO methods

# Load all tasks from the JSON file
def load_tasks(tasks_fp: str = TASKS_PATH) -> dict:
    try:
        with open(tasks_fp, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("JSON root is not a dict")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Load a single task by ID
def load_task(id: int, tasks_fp: str = TASKS_PATH):
    try:
        with open(tasks_fp, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("JSON root is not a dict")
            task = data.get(str(id))
            if not task:
                print(f"Task with id: {id} does not exist")
                return
            return task
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save all tasks to the JSON file
def save_tasks(tasks: dict, tasks_fp: str = TASKS_PATH) -> None:
    with open(tasks_fp, 'w') as file:
        json.dump(tasks, file, indent=4)

#endregion

# Format a timestamp to human-readable format
def format_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

# Parse user input into a list of command components
def process_line(line: str):
    if line.startswith("add"):
        cmd = "add"
        rest = line[4:].strip()
        if rest.startswith('"') and rest.endswith('"'):
            desc = rest[1:-1]
            return [cmd, desc]

    elif line.startswith("update "):
        cmd = "update"
        id_and_desc = line[6:].strip()
        first_space = id_and_desc.find(" ")
        task_id = id_and_desc[0:first_space]
        try:
            _ = int(task_id)
        except:
            print(f"Id: {task_id} is invalid. How did this happen...")
        desc_part = id_and_desc[first_space:].strip()
        if desc_part.startswith('"') and desc_part.endswith('"'):
            desc = desc_part[1:-1]
            return [cmd, task_id, desc]

    return line.split()

# Add a new task with the given description
def add_task(description: str) -> None:
    tasks = load_tasks()
    current_time = time.time()
    task = {
        "desc": description.strip("\""),
        "status": Status.TODO.value,
        "createdAt": current_time,
        "updatedAt": current_time,
    }
    next_unique_id = max(map(int, tasks.keys()), default=0) + 1
    tasks.update({next_unique_id: task})
    save_tasks(tasks)

# Update the description of an existing task
def update_task(id: int, new_description: str) -> None:
    tasks = load_tasks()
    id = str(id)
    if id in tasks:
        tasks[id].update({
            "desc": new_description,
            "updatedAt": time.time()
        })
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

# Delete a task by ID
def delete_task(id: int) -> None:
    tasks = load_tasks()
    id = str(id)
    if id in tasks:
        del tasks[id]
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

# Mark a task as in progress
def mark_in_progress(id: int) -> None:
    tasks = load_tasks()
    id = str(id)
    if id in tasks:
        tasks[id]["status"] = Status.IN_PROGRESS.value
        tasks[id]["updatedAt"] = time.time()
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

# Mark a task as done
def mark_done(id: int) -> None:
    tasks = load_tasks()
    id = str(id)
    if id in tasks:
        tasks[id]["status"] = Status.DONE.value
        tasks[id]["updatedAt"] = time.time()
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

# List tasks, optionally filtered by status
def list_tasks(type: int = None) -> None:
    tasks = load_tasks()
    if type == "done":
        type = Status.DONE.value
    elif type == "todo":
        type = Status.TODO.value
    elif type == "in-progress":
        type = Status.IN_PROGRESS.value
    elif type is not None:
        print(f"Invalid type: {type}. Valid choices: 'done', 'todo', 'in-progress'")
        return

    if type is not None:
        tasks = dict(filter(lambda item: item[1].get("status") == type, tasks.items()))

    for task_id, task in tasks.items():
        print(f"Task #{task_id}: {task.get('desc')}")
        print(f"Status: {task.get('status')}")
        print(f"Created at: {format_time(task.get('createdAt'))}")
        print(f"Last updated at: {format_time(task.get('updatedAt'))}")
        print()

# Display help message with available commands
def show_help():
    print("Available commands:")
    print("  add \"task description\"")
    print("  update <id> \"new description\"")
    print("  delete <id>")
    print("  mark-in-progress <id>")
    print("  mark-done <id>")
    print("  list [todo|in-progress|done]")
    print("  help")
    print("  exit")

# Main REPL loop for the CLI application
def main():
    while True:
        line = input("task-cli ")
        line = process_line(line)
        if not line or len(line) == 0:
            print("No command entered.")
            continue

        match line[0]:
            case "add":
                add_task(line[1])
            case "update":
                update_task(line[1], line[2])
            case "delete":
                delete_task(line[1])
            case "mark-in-progress":
                mark_in_progress(line[1])
            case "mark-done":
                mark_done(line[1])
            case "list":
                if len(line) == 1:
                    list_tasks()
                elif len(line) == 2:
                    list_tasks(line[1])
                else:
                    print("Invalid number of arguments for 'list' function.")
            case "help":
                show_help()
            case "exit":
                break
            case _:
                print("Invalid command, try again")

# Entry point
if __name__ == "__main__":
    main()
