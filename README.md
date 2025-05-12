# 🐍 Learning-Python

> A collaborative journey into Python by KelpFriesOG & Tataby

This repository documents our learning adventure through Python — from foundational concepts to real-world projects. 

---

## 📁 Repo Structure

```
Learning-Python/
├── notes/        ← Organized, progressive Jupyter notebooks
└── projects/     ← Applied, hands-on Python projects
```

---

## 📝 Notes: Kalp's Track

All notebooks in the `notes/` directory are numbered and build sequentially. These are my personal notes — structured, annotated, and aimed at long-term understanding.

| No. | Notebook File                             | Topic                                |
|-----|--------------------------------------------|--------------------------------------|
| 01  | `01_getting_started.ipynb`                 | Python setup, syntax basics          |
| 02  | `02_basic_python_structures.ipynb`         | Control flow, loops, exceptions      |
| 03  | `03_functions_and_type_hinting.ipynb`      | Functions, nesting, type hints       |
| 04  | `04_string_and_array_manipulation.ipynb`   | Strings, lists, comprehensions       |
| 05  | `05_additional_data_structures.ipynb`      | Tuples, sets, dictionaries, frozenset|
| 06  | `06_oop_fundamentals.ipynb`                | Classes, instantiation, inheritance  |
| 07  | `07_dunder_functions_and_variables.ipynb`  | Special methods like `__repr__`, `__init__` |
| 08  | `08_abstract_classes_and_interfaces.ipynb` | ABCs, interface-like behavior        |

🧠 **More topics coming soon**: modules, file I/O, decorators, generators, and testing!

---

## 🧪 Projects

The `projects/` directory includes real-world tasks and mini-apps based on [roadmap.sh/python projects](https://roadmap.sh/projects/task-tracker).

### ✅ Currently Active

- **Task Tracker** – A CLI-based to-do app that saves tasks in a JSON file and supports add/update/delete/query via command line.

```bash
$ python task-cli.py add "Buy groceries"
$ python task-cli.py list
```

🛠 Built with:
- File I/O
- Dictionary-based task storage
- argparse (coming soon)
- Persistent state via JSON

---

## 🤝 Collaboration Workflow

- We're working on separate branches to reflect our personal tracks.
- Feel free to compare implementations, raise issues, or suggest improvements!
- Kalp's branch: `kalp`
- KelpFriesOG’s branch: `main` or custom

---

## 📦 Setup Instructions

```bash
git clone https://github.com/<your-username>/Learning-Python.git
cd Learning-Python
pip install notebook
jupyter notebook
```

Or run projects with:
```bash
cd projects/task-tracker
python task-cli.py list
```

---

## 💬 Why This Exists

We didn’t just want to "learn Python" — we wanted to understand it. Really understand it. This repo is our proof-of-work: curious, critical, and constantly evolving.

> This is **Kalp’s side** of the journey — the experiments, the notes, and the occasional detour 🌱