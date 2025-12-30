# Expense Tracker (Flask + SQLite)

## Overview
This project is a **local-first Expense Tracker** built using **Python, Flask, and SQLite**. It started as a **CLI-based application** and was later extended into a **web application** without rewriting the core business logic.

The primary goal of this project is to demonstrate **software engineering fundamentals**:
- Separation of concerns
- Reuse of business logic across interfaces
- Data persistence and aggregation
- Simple but meaningful system design

This is **not** a cloud-based or production-deployed system. It is intentionally local and lightweight.

---

## Features

- Add expenses (date, category, note, amount)
- View expense summary by category
- Dashboard view with aggregated data
- Monthly expense report
- Identify category with maximum spending
- Clear expenses (controlled deletion)
- Persistent storage using SQLite

---

## Project Structure

```
expense-tracker/
│
├── app.py                 # Flask application (routes + integration layer)
├── logic/                 # Core business logic (pure Python)
│   ├── db.py              # Database connection and queries
│   ├── expense_service.py # Expense operations (add, read, aggregate, clear)
│
├── templates/             # HTML templates (Jinja2)
│   ├── index.html
│   ├── dashboard.html
│
├── static/                # Basic CSS styling
│   └── style.css
│
├── instance/              # Runtime data (Flask-managed)
│   └── Expense.db         # SQLite database
│
├── requirements.txt
├── README.md
```

---

## Logic Folder (Important)

The `logic/` folder contains the **core application logic written in plain Python**.

This logic:
- Does **not** depend on Flask
- Can be reused by a CLI, scripts, or tests
- Handles all database operations and calculations

Originally, the project existed **only as a CLI application** using the same logic. The Flask app simply imports and uses these functions.

This design ensures:
- Business rules are not tied to the web framework
- The application can evolve without rewriting logic
- Clear separation between **interface** and **behavior**

---

## Why Flask

Flask was chosen because:
- It is lightweight and explicit
- It fits small-to-medium internal tools
- It allows direct control over architecture

No frontend frameworks or JavaScript libraries were used. The UI exists only to expose backend functionality.

---

## Why SQLite

SQLite was chosen because:
- It is file-based and requires no setup
- It is suitable for single-user or low-concurrency tools
- It integrates cleanly with Flask

The database is stored in the `instance/` directory, following Flask best practices for writable runtime data.

---

## How to Run Locally

1. Create a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open the browser at:
   ```
   http://127.0.0.1:5000
   ```

---

## Clear Expense Behavior

The **Clear Expense** option deletes expense records from the database.

Current behavior:
- Clears all stored expenses
- Intended for reset/testing scenarios

This operation is intentionally explicit to avoid accidental data loss.

---

## Limitations

- No authentication or multi-user support
- SQLite has limited concurrency support
- No deployment or cloud configuration
- Minimal frontend styling

These limitations are accepted by design.

---

## Scaling Considerations

If this system were scaled:
- SQLite would be replaced with PostgreSQL
- Database access would use connection pooling
- Clear operations would be scoped (by user or month)
- Authentication and authorization would be introduced

---

## Engineering Focus

This project prioritizes:
- Correctness over features
- Architecture over polish
- Understanding over tutorials

It is intentionally simple, complete, and well-scoped.

