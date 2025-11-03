# CLI Task Tracker

A powerful command-line task tracker built with Python.  
Features color-coded output using [Colorama](https://pypi.org/project/colorama/) for better readability and SQLite for data persistence.

---

## Features

- Add tasks with priority (Low/Medium/High) and due dates ✅
- List tasks with advanced filtering and sorting:
  - Sort by due date or creation date
  - Filter by status (Pending/Done)
  - **Green ✅** = Done
  - **Yellow ⚠️** = Pending
- Edit task details (description, due date, status, priority) 📝
- Bulk actions - operate on multiple tasks or all tasks at once
- Mark tasks as done 🎉
- Delete tasks 🗑️
- Search tasks by keyword 🔍
- Color-coded output for better visibility
- SQLite database for reliable data storage

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/Bojiii28/Python-CLI-Task-Tracker.git
cd Python-CLI-Task-Tracker
```

2. Install dependencies:

```bash
pip install colorama
```

---

## Usage

### Add a task

```bash
python task.py add "Learn Python" --due 2025-12-31 --priority High
```

### List tasks

```bash
# List all tasks
python task.py list

# Sort by due date
python task.py list --sort due

# Filter by status
python task.py list --status Done
```

### Edit tasks

```bash
# Edit a single task
python task.py edit 1 --desc "New description" --due 2025-12-31 --priority High

# Edit multiple tasks
python task.py edit 1 2 3 --status Done

# Edit all tasks
python task.py edit all --priority High
```

### Mark tasks as done

```bash
# Mark specific tasks as done
python task.py done 1 2 3

# Mark all tasks as done
python task.py done all
```

### Delete tasks

```bash
# Delete specific tasks
python task.py delete 1 2 3

# Delete all tasks
python task.py delete all
```

### Search tasks

```bash
python task.py search "python"
```

### Help

```bash
python task.py help
```

---

## How the Colors Work

| Color      | Meaning                 |
| ---------- | ----------------------- |
| Green ✅   | Task added or completed |
| Yellow ⚠️  | Pending tasks           |
| Red ❌     | Errors or missing tasks |
| Cyan 🎉    | Task marked done        |
| Blue ✏️    | Task updated            |
| Magenta 🗑️ | Task deleted            |

---

## Project Structure

```
CLI Task Tracker/
├─ task.py     # Main CLI script
├─ tasks.db    # SQLite database
```

---

## Features Added

- ✅ SQLite database for better data persistence
- ✅ Task priorities (Low/Medium/High)
- ✅ Due dates with validation
- ✅ Advanced listing with sorting and filtering
- ✅ Bulk actions (edit/delete/complete multiple tasks)
- ✅ Search functionality
- ✅ Improved help command with color-coded documentation
- ✅ Task editing functionality
- ✅ Display numbers for better task management

---

## Author

Bojiii28
