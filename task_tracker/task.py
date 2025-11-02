import json
import argparse
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("tasks.json")

# File Handler Functions
def load_tasks():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file: # Read mode
            return json.load(file)
    return []

# Save Tasks
def save_tasks(tasks):
    with open(DATA_FILE, "w") as file: # Write mode
        json.dump(tasks, file, indent=4)
        
# Add Tasks
def add_task(description):
    tasks = load_tasks()
    
    new_task = {
        "id": len(tasks) + 1, # Unique ID
        "description": description,
        "status": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Readable timestamp
    }
    
    tasks.append(new_task)
    save_tasks(tasks) # Updates the file
    print(f"✅ Task added: {description}")
    
# List All Tasks
def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"[{task['id']}] {task['description']} - {task['status']}")
        
# Update Tasks
def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "Done"
            save_tasks(tasks)
            print(f"🎉 Task {task_id} marked as done.")
            return
    print("❎ Task not found.")

# Delete Tasks
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t["id"] != task_id]
    if len(updated_tasks) == len(tasks):
        print("❎ Task not found.")
        return
    save_tasks(updated_tasks)
    print(f"🗑️ Task {task_id} deleted.")
    
# Command Parser
def main():
    # Create the main parser and give it a short description
    parser = argparse.ArgumentParser(description="Simple CLI Task Tracker")
    
    # Add a group of subcommands (add, list, done, delete)
    subparsers = parser.add_subparsers(dest="command")

    # ---------------- ADD COMMAND ----------------
    # Create a parser for the "add" command
    add_parser = subparsers.add_parser("add")
    # Add a required argument (task description)
    add_parser.add_argument("description", type=str, help="Task description")

    # ---------------- LIST COMMAND ----------------
    # Create a parser for the "list" command (no extra arguments)
    subparsers.add_parser("list")

    # ---------------- DONE COMMAND ----------------
    # Create a parser for the "done" command
    done_parser = subparsers.add_parser("done")
    # Add a required integer argument for task ID
    done_parser.add_argument("id", type=int, help="Task ID")

    # ---------------- DELETE COMMAND ----------------
    # Create a parser for the "delete" command
    delete_parser = subparsers.add_parser("delete")
    # Add a required integer argument for task ID
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Parse all command-line arguments entered by the user
    args = parser.parse_args()

    # ---------------- COMMAND HANDLER ----------------
    # Match the command and call the correct function
    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    else:
        # If no valid command, show the help message
        parser.print_help()

# Run the main() function only when this script is executed directly
if __name__ == "__main__":
    main()


    
