````markdown
# CLI Task Tracker

A simple command-line task tracker built with Python.  
Includes color-coded output using [Colorama](https://pypi.org/project/colorama/) for better readability.

---

## Features

- Add tasks ✅
- List tasks with status:
  - **Green ✅** = Done
  - **Yellow ⚠️** = Pending
- Mark tasks as done 🎉
- Delete tasks 🗑️
- Color-coded error messages ❌

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/Bojiii28/Python-CLI-Task-Tracker.git
cd Python-CLI-Task-Tracker/task_tracker
```
````

2. Install dependencies:

```bash
pip install colorama
```

---

## Usage

### Add a task

```bash
python task.py add "Learn Python"
```

### List all tasks

```bash
python task.py list
```

### Mark a task as done

```bash
python task.py done 1
```

### Delete a task

```bash
python task.py delete 1
```

---

## How the Colors Work

| Color      | Meaning                 |
| ---------- | ----------------------- |
| Green ✅   | Task added or completed |
| Yellow ⚠️  | Pending tasks           |
| Red ❌     | Errors or missing tasks |
| Cyan 🎉    | Task marked done        |
| Magenta 🗑️ | Task deleted            |

---

## Project Structure

```
task_tracker/
├─ task.py          # Main CLI script
├─ tasks.json       # Stores task data
```

---

## Next Steps / Improvements

- Add search functionality
- Add due dates
- Replace JSON with SQLite for database persistence

---

## Author

Bojiii28
