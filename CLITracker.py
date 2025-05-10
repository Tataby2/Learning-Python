
''' 
Add, Update, and Delete tasks
Mark a task as in progress or done
List all tasks
List all tasks that are done
List all tasks that are not done
List all tasks that are in progress
Here are some constraints to guide the implementation:
Use positional arguments in command line to accept user inputs.
Use a JSON file to store the tasks in the current directory.
The JSON file should be created if it does not exist.
Use the native file system module of your programming language to interact with the JSON file.
Do not use any external libraries or frameworks to build this project.
Ensure to handle errors and edge cases gracefully.
'''
#importing the json and time modules
import json
import time

# lists can store multiple data types
#in this case tasks is a global variable
tasks = list()

def load_tasks(file):
    tasks = json.load(file)
    return tasks

def add_task(msg: str) -> None:   #The arrow means that the function returns nothing (type hinting is optional), Python does not require setting a return type
    #Get user input         #To create a function use def
    #Python does not require setting data type to a variable
    #The text in the input box is a string that will prompt the user with whatever is written in the input box
    
    tasks.append(msg)
    
    # Step 1: Create a dictionary with the following attributes:
    # id, description, status, createdAt, updatedAt
    task = {
        "id" : 1,
        # e.t.c.
    }

def update_task():
    pass

def delete_task():
    pass
    
def main():

    print("Welcome to Task Tracker CLI")
    print("Created by Kalpesh and Aabaan Samad\n")
    
    
    # Step 1: Parse input into tokens using .split() function
    user_input = input()
    user_input = user_input.split()
    
    # Step 2: Ensure input starts with task-cli (if statement)
    if user_input[0] == "task-cli":
        if user_input[1] == "add":
            add_task()
        if user_input[1] == "update":
            update_task()
        if user_input[1] == "delete":
            delete_task()
        if user_input[1] == "mark-in-progress":
            pass
        if user_input[1] == "mark-done":
            pass
        if user_input[1] == "list":
            if user_input[2] == "done":
                pass
            if user_input[2] == "todo":
                pass
            if user_input[2] == "in-progress":
                pass
        if user_input[1] == "exit":
            pass   
    # If not send invalid input message
    else:
        print("Error!")

    pass


if __name__ == "__main__": #this will run the main function
    main()
    
