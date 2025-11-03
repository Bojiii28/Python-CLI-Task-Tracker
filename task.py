import sqlite3
import argparse
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)  # Enable colored output

DB_FILE = "tasks.db"  # SQLite database file

# ------------------- DATABASE -------------------
def init_db():
    """Create DB and tasks table. Add priority column if missing."""
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
    # Add priority column if not exists
    c.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in c.fetchall()]
    if "priority" not in columns:
        c.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'")
    conn.commit()
    conn.close()


# ------------------- VALIDATE DUE DATE -------------------
def validate_due_date(due_date):
    """Check if due date is YYYY-MM-DD."""
    if due_date is None:
        return None
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return due_date
    except ValueError:
        print(Fore.RED + "❌ Invalid date format. Use YYYY-MM-DD.")
        return None


# ------------------- ADD TASK -------------------
def add_task(description, due_date=None, priority="Medium"):
    """Add a new task with optional due date and priority."""
    if due_date:
        due_date = validate_due_date(due_date)
        if due_date is None:
            return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO tasks (description, status, created_at, due_date, priority)
        VALUES (?, 'Pending', ?, ?, ?)
    ''', (description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), due_date, priority))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Task added: {description} ({priority})")


# ------------------- LIST TASKS -------------------
def list_tasks(sort_by=None, filter_status=None):
    """Show all tasks with sequential numbers for display, keep DB IDs for commands."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT * FROM tasks"
    params = []

    if filter_status:
        query += " WHERE status = ?"
        params.append(filter_status.capitalize())

    if sort_by == "due":
        query += " ORDER BY due_date ASC"
    else:
        query += " ORDER BY created_at ASC"

    c.execute(query, params)
    tasks = c.fetchall()
    conn.close()

    if not tasks:
        print(Fore.RED + "No tasks found.")
        return

    for idx, t in enumerate(tasks, start=1):
        task_id, description, status, created_at, due_date, priority = t
        color = Fore.GREEN if status == "Done" else Fore.YELLOW
        due_text = f" - Due: {due_date}" if due_date else ""
        print(f"{color}[{idx}] {description} - {status} ({priority}){due_text} (ID:{task_id}){Style.RESET_ALL}")
        
# ------------------- GET TASK IDS BY DISPLAY -------------------
def get_task_ids_by_display(display_numbers, sort_by=None, filter_status=None):
    """Map display numbers to real DB IDs."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = "SELECT id FROM tasks"
    params = []

    if filter_status:
        query += " WHERE status = ?"
        params.append(filter_status.capitalize())

    if sort_by == "due":
        query += " ORDER BY due_date ASC"
    else:
        query += " ORDER BY created_at ASC"

    c.execute(query, params)
    all_ids = [row[0] for row in c.fetchall()]
    conn.close()

    selected_ids = []
    for num in display_numbers:
        if 0 < num <= len(all_ids):
            selected_ids.append(all_ids[num-1])
        else:
            print(Fore.RED + f"❌ Task number {num} not found.")
    return selected_ids

# ------------------- COMPLETE TASK -------------------
def complete_task(task_ids):
    """Mark task as Done."""
    if not task_ids:
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for task_id in task_ids:
        c.execute("UPDATE tasks SET status='Done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    print(Fore.CYAN + f"🎉 {len(task_ids)} task(s) marked as done.")


# ------------------- EDIT TASK -------------------
def edit_task(task_ids, new_description=None, new_due_date=None, new_status=None, new_priority=None):
    """Update task fields provided by user."""
    if not task_ids:
        return
    if new_due_date:
        new_due_date = validate_due_date(new_due_date)
        if new_due_date is None:
            return

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for task_id in task_ids:
        updates = []
        params = []

        if new_description:
            updates.append("description = ?")
            params.append(new_description)
        if new_due_date:
            updates.append("due_date = ?")
            params.append(new_due_date)
        if new_status:
            updates.append("status = ?")
            params.append(new_status.capitalize())
        if new_priority:
            updates.append("priority = ?")
            params.append(new_priority)

        if not updates:
            print(Fore.RED + "❌ Nothing to update.")
            continue

        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        params.append(task_id)
        c.execute(query, params)
        if c.rowcount == 0:
            print(Fore.RED + f"❌ Task {task_id} not found.")
        else:
            print(Fore.BLUE + f"✏️ Task {task_id} updated.")
    conn.commit()
    conn.close()


# ------------------- DELETE TASK -------------------
def delete_task(task_ids):
    """Delete task by ID."""
    if not task_ids:
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for task_id in task_ids:
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    print(Fore.MAGENTA + f"🗑️ {len(task_ids)} task(s) deleted.")


# ------------------- SEARCH TASK -------------------
def search_tasks(keyword):
    """Search tasks by keyword."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE description LIKE ?", ('%' + keyword + '%',))
    results = c.fetchall()
    conn.close()

    if not results:
        print(Fore.RED + "❌ No tasks found.")
        return

    for idx, t in enumerate(results, start=1):
        task_id, description, status, created_at, due_date, priority = t
        color = Fore.GREEN if status == "Done" else Fore.YELLOW
        due_text = f" - Due: {due_date}" if due_date else ""
        print(f"{color}[{idx}] {description} - {status} ({priority}){due_text}{Style.RESET_ALL}")
        
# ------------------- HELP COMMAND -------------------
def show_help():
    """Show all available commands."""
    print(Fore.CYAN + "📖 Available commands:\n")
    print(Fore.YELLOW + "add <description> [--due YYYY-MM-DD] [--priority Low|Medium|High]")
    print("    Add a new task.\n")
    print(Fore.YELLOW + "list [--sort due|created] [--status Pending|Done]")
    print("    List tasks.\n")
    print(Fore.YELLOW + "edit <numbers>|all [--desc <desc>] [--due YYYY-MM-DD] [--status Pending|Done] [--priority Low|Medium|High]")
    print("    Edit tasks by display numbers or all tasks.\n")
    print(Fore.YELLOW + "delete <numbers>|all")
    print("    Delete tasks by display numbers or all.\n")
    print(Fore.YELLOW + "done <numbers>|all")
    print("    Mark tasks as done by display numbers or all.\n")
    print(Fore.YELLOW + "search <keyword>")
    print("    Search tasks by keyword.\n")
    print(Fore.YELLOW + "help")
    print("    Show this help message.\n")


# ------------------- CLI HANDLER -------------------
def main():
    init_db()
    parser = argparse.ArgumentParser(description="Advanced CLI Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser(
        "add", help="Add a new task with optional due date and priority"
    )
    add_parser.add_argument("description", type=str, help="Task description")
    add_parser.add_argument("--due", type=str, help="Due date YYYY-MM-DD")
    add_parser.add_argument("--priority", choices=["Low","Medium","High"], default="Medium", help="Task priority")

    # List
    list_parser = subparsers.add_parser(
        "list", help="List all tasks with optional sorting and filtering"
    )
    list_parser.add_argument("--sort", choices=["due","created"], help="Sort by due or creation date")
    list_parser.add_argument("--status", choices=["Pending","Done"], help="Filter by status")

    # Edit
    edit_parser = subparsers.add_parser(
        "edit", help="Edit one or more tasks by display number or 'all'"
    )
    edit_parser.add_argument("numbers", nargs="+", help="Task number(s) or 'all'")
    edit_parser.add_argument("--desc", type=str, help="New description")
    edit_parser.add_argument("--due", type=str, help="New due date YYYY-MM-DD")
    edit_parser.add_argument("--status", choices=["Pending","Done"], help="New status")
    edit_parser.add_argument("--priority", choices=["Low","Medium","High"], help="New priority")

    # Delete
    delete_parser = subparsers.add_parser(
        "delete", help="Delete tasks by display number(s) or 'all'"
    )
    delete_parser.add_argument("numbers", nargs="+", help="Task number(s) or 'all'")

    # Done
    done_parser = subparsers.add_parser(
        "done", help="Mark tasks as done by display number(s) or 'all'"
    )
    done_parser.add_argument("numbers", nargs="+", help="Task number(s) or 'all'")

    # Search
    search_parser = subparsers.add_parser(
        "search", help="Search tasks by keyword"
    )
    search_parser.add_argument("keyword", help="Keyword to search for")

    # Help
    subparsers.add_parser(
        "help", help="Show full colored help with all commands"
    )

    args = parser.parse_args()

    # ---------------- COMMAND HANDLING ----------------
    if args.command == "add":
        add_task(args.description, args.due, args.priority)
        
    elif args.command == "list":
        list_tasks(args.sort, args.status)
        
    elif args.command == "edit":
            if "all" in args.numbers:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("SELECT id FROM tasks")
                ids = [row[0] for row in c.fetchall()]
                conn.close()
            else:
                try:
                    nums = [int(n) for n in args.numbers]
                except ValueError:
                    print(Fore.RED + "❌ Task numbers must be integers.")
                    return
                ids = get_task_ids_by_display(nums)
            edit_task(ids, args.desc, args.due, args.status, args.priority)
            
    elif args.command == "delete":
        if "all" in args.numbers:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT id FROM tasks")
            ids = [row[0] for row in c.fetchall()]
            conn.close()
        else:
            try:
                nums = [int(n) for n in args.numbers]
            except ValueError:
                print(Fore.RED + "❌ Task numbers must be integers.")
                return
            ids = get_task_ids_by_display(nums)
        delete_task(ids)
        
    elif args.command == "done":
        if "all" in args.numbers:
            # Mark all tasks done
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("SELECT id FROM tasks WHERE status != 'Done'")
            ids = [row[0] for row in c.fetchall()]
            conn.close()
        else:
            try:
                nums = [int(n) for n in args.numbers]
            except ValueError:
                print(Fore.RED + "❌ Task numbers must be integers.")
                return
            ids = get_task_ids_by_display(nums)
        complete_task(ids)
        
    elif args.command == "search":
        search_tasks(args.keyword)
        
    elif args.command == "help" or args.command is None:
        show_help()
        
    else:
        parser.print_help()


# ------------------- RUN -------------------
if __name__ == "__main__":
    main()
