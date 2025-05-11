from enum import Enum
import json, time
import os

# Got help from GPT for this one
TASKS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


#region Task IO methods

def load_tasks(tasks_fp: str = TASKS_PATH) -> dict:
    try:
        with open(tasks_fp, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("JSON root is not a dict")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Start fresh if file doesn't exist

def load_task(id: int, tasks_fp: str = TASKS_PATH):
    try:
        with open(tasks_fp, 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("JSON root is not a dict")
            task = data.get(id)
            if not task:
                print(f"Task with id: {id} does not exist")
                return
            return task
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}  # Start fresh if file doesn't exist

def save_tasks(tasks: dict, tasks_fp: str = TASKS_PATH) -> None:
    with open(tasks_fp, 'w') as file:
        json.dump(tasks, file, indent=4)

#endregion

def process_line(line: str):
    
    if line.startswith("add "):
        cmd = "add"
        rest = line[4:].strip()
        if rest.startswith('"') and rest.endswith('"'):
            desc = rest[1:-1]
            return [cmd, desc]

    elif line.startswith("update "):
        cmd = "update"
        # Find the first space after "update "
        first_space = line.find(" ", 7)
        if first_space == -1:
            return [cmd]  # incomplete input
        task_id = line[7:first_space].strip()
        desc_part = line[first_space:].strip()
        if desc_part.startswith('"') and desc_part.endswith('"'):
            desc = desc_part[1:-1]
            return [cmd, task_id, desc]

    # fallback: naive split
    return line.split()


def add_task(description: str) -> None:    

    # Load in the dictionary of all tasks
    tasks = load_tasks()

    # Create the values associated with the task (which themselves will be a dictionary)
    # i.e. a dictionary within a dictionary
    current_time = time.time()
    task = {
        "desc": description.strip("\""),
        "status": 0, # 0 meaning todo
        "createdAt": current_time,
        "updatedAt": current_time,
    }

    # What is the next unique id? Well its one greater than the current highest
    # unique id to be safe!
    next_unique_id = max(map(int, tasks.keys()), default=0) + 1

    # Add the task to the dictionary of tasks with the next
    # available unique id.
    tasks.update({next_unique_id : task})

    # Dump the changed information back into the json (save)
    save_tasks(tasks)

def update_task(id: int, new_description: str) -> None:
    
    # Load in the dictionary of all tasks
    tasks = load_tasks()
    
    # Only update the updatedAt parameter of the value of our task (if it exists)
    if id in tasks:
        tasks[id].update({
            "desc": new_description,
            "updatedAt": time.time()
        })
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

def delete_task(id: int) -> None:
    
    # Load in the dictionary of all tasks
    tasks = load_tasks()
    
    # If the tasks have the id, then only can we delete something
    if id in tasks:
        del tasks[id]
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

def list_tasks(type: int = None) -> None:

    # List all the tasks by iterating through the dictionary object, and filter
    # based on the type

    tasks = load_tasks()

    if type:
        tasks = dict(filter(lambda item: item['status'] == type, tasks.items()))

    print(tasks)

def main():

    while True:
        
        # Step 1: Read and tokenize input
        line = input("task-cli ")
        line = process_line(line)

        # Step 2: Interpret first token
        match line[0]:
            case "add":
                add_task(line[1])
            case "update":
                update_task(line[1], line[2])
                pass
            case "delete":
                delete_task(line[1])
            case "mark-in-progress":
                pass
            case "mark-done":
                pass
            case "list":
                pass
            case _:
                print("Invalid command, try again")


if __name__ == "__main__":
    main()