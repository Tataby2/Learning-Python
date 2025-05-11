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
            # Convert the id to a string and find a match
            task = data.get(str(id))
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
    
    if line.startswith("add"):
        cmd = "add"
        rest = line[4:].strip() # "hello world"
        if rest.startswith('"') and rest.endswith('"'):
            desc = rest[1:-1] # hello world
            return [cmd, desc]

    elif line.startswith("update "):
        cmd = "update"
        
        id_and_desc = line[6:]
        id_and_desc = id_and_desc.strip()
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

        # # Find the first space after "update "
        # first_space = line.find(" ", 7)
        # # DEAL WITH MALFORMATTED USER INPUT
        # if first_space == -1:
        #     return [cmd]  # incomplete input
        # task_id = line[7:first_space].strip()
        # desc_part = line[first_space:].strip()
        # if desc_part.startswith('"') and desc_part.endswith('"'):
        #     desc = desc_part[1:-1]
        #     return [cmd, task_id, desc]

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
    id = str(id)
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
    # Convert id to string
    id = str(id)

    # If the tasks have the id, then only can we delete something
    if id in tasks:
        del tasks[id]
        save_tasks(tasks)
    else:
        print(f"No task found with ID: {id}")

def mark_in_progress(id: int) -> None:

    # # Gives me the details for the task (dictionary)
    # task = load_task()

    # # Mark the status property in the dictionary as being 1 (in progress)
    # task["status"] = "1"

    # # Load in all the tasks, and then set the values for our task to be the updated values (changed status)
    # tasks = load_tasks
    # tasks[str(id)] = task

    # save_tasks(tasks)

    tasks = load_tasks()
    tasks[str(id)]["status"] = 1
    save_tasks(tasks)

    pass

def mark_done(id: int) -> None:

    tasks = load_tasks()
    tasks[str(id)]["status"] = 2
    save_tasks(tasks)

    pass

def list_tasks(type: int = None) -> None:

    # List all the tasks by iterating through the dictionary object, and filter
    # based on the type

    tasks = load_tasks()

    if type == "done":
        type = 2
    elif type == "todo":
        type = 0
    elif type == "in-progress":
        type = 1
    elif type != None:
        print(f"Invalid type: {type}. Valid choices: 'done', 'todo', 'in-progress'")
        return

    if type != None:
        tasks = dict(filter(lambda item: item[1].get("status") == type, tasks.items()))

    for task_id, task in tasks.items():
        print(f"Task #{task_id}: {task.get("desc")}")
        print(f"Status: {task.get("status")}")
        print(f"Created at: {task.get("createdAt")}")
        print(f"Last updated at: {task.get("updatedAt")}")
        print()

def main():

    while True:
        
        # Step 1: Read and tokenize input
        line = input("task-cli ")
        line = process_line(line)

        # if line[0] == "add":
        #     pass
        # elif line[0] == "update":
        #     pass
        # # ...
        # else:
        #     print("Invalid command, try again")

        # Step 2: Interpret first token
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
            case _:
                print("Invalid command, try again")


if __name__ == "__main__":
    main()