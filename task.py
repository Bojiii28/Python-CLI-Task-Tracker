import sqlite3
import argparse
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama for colored CLI output
init(autoreset=True)

# Define database file name
DB_FILE = "tasks.db"

# -----------------------------------------------------------
# 1. DATABASE INITIALIZATION
# -----------------------------------------------------------
def init_db():
    """
    Creates a SQLite database file (tasks.db) if it doesn't exist.
    Inside it, creates a 'tasks' table to store all your task info.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT,
            due_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

# -----------------------------------------------------------
# 2. ADD TASK
# -----------------------------------------------------------
def add_task(description, due_date=None):
    """
    Inserts a new task into the database.
    If a due date is given, it stores that too.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (description, status, created_at, due_date)
        VALUES (?, 'Pending', ?, ?)
    ''', (description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), due_date))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Task added: {description}")

# -----------------------------------------------------------
# 3. LIST TASKS
# -----------------------------------------------------------
def list_tasks():
    """
    Fetches and displays all tasks from the database.
    Color codes them based on status.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()

    if not tasks:
        print(Fore.RED + "No tasks found.")
        return

    for task in tasks:
        id, description, status, created_at, due_date = task
        color = Fore.GREEN if status == "Done" else Fore.YELLOW
        due_text = f" - Due: {due_date}" if due_date else ""
        print(f"{color}[{id}] {description} - {status}{due_text}{Style.RESET_ALL}")

# -----------------------------------------------------------
# 4. COMPLETE TASK
# -----------------------------------------------------------
def complete_task(task_id):
    """
    Marks a specific task as 'Done' based on its ID.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()

    if c.rowcount == 0:
        print(Fore.RED + "❌ Task not found.")
    else:
        print(Fore.CYAN + f"🎉 Task {task_id} marked as done.")
    conn.close()

# -----------------------------------------------------------
# 5. DELETE TASK
# -----------------------------------------------------------
def delete_task(task_id):
    """
    Permanently removes a task from the database.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

    if c.rowcount == 0:
        print(Fore.RED + "❌ Task not found.")
    else:
        print(Fore.MAGENTA + f"🗑️ Task {task_id} deleted.")
    conn.close()

# -----------------------------------------------------------
# 6. SEARCH TASK
# -----------------------------------------------------------
def search_tasks(keyword):
    """
    Searches for tasks that contain the given keyword in their description.
    Uses the SQL 'LIKE' operator for partial matches.
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE description LIKE ?", ('%' + keyword + '%',))
    results = c.fetchall()
    conn.close()

    if not results:
        print(Fore.RED + "❌ No tasks found.")
        return

    for t in results:
        color = Fore.GREEN if t[2] == "Done" else Fore.YELLOW
        print(f"{color}[{t[0]}] {t[1]} - {t[2]} - Due: {t[4]}{Style.RESET_ALL}")

# -----------------------------------------------------------
# 7. COMMAND LINE HANDLER
# -----------------------------------------------------------
def main():
    """
    The command-line interface that handles all user commands.
    Uses argparse to parse 'add', 'list', 'done', 'delete', and 'search' commands.
    """
    init_db()  # Ensure database and table exist

    parser = argparse.ArgumentParser(description="Simple CLI Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new task with optional due date")
    add_parser.add_argument("description", type=str, help="Task description")
    add_parser.add_argument("--due", type=str, help="Optional due date (YYYY-MM-DD)")

    # List
    subparsers.add_parser("list", help="List all tasks")

    # Done
    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("id", type=int, help="Task ID")

    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # Search
    search_parser = subparsers.add_parser("search", help="Search tasks by keyword")
    search_parser.add_argument("keyword", type=str, help="Keyword to search for")

    # Parse arguments
    args = parser.parse_args()

    # Command Handler
    if args.command == "add":
        add_task(args.description, args.due)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "search":
        search_tasks(args.keyword)
    else:
        parser.print_help()

# -----------------------------------------------------------
# 8. RUN THE PROGRAM
# -----------------------------------------------------------
if __name__ == "__main__":
    main()
