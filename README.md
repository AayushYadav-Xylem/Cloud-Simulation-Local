# 🌐 Local Cloud Simulation — Event Registration App

> A locally-running web application that simulates real cloud architecture using **Flask**, **SQLite**, and **HTML/JavaScript**. Built to demonstrate how client-server communication, REST APIs, and databases work — mirroring the exact patterns used by platforms like Google Cloud Run, Firebase, and AWS Lambda.

---

## 📌 Table of Contents

- [What is this project?](#what-is-this-project)
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Running the App](#running-the-app)
- [Pages & Routes](#pages--routes)
- [Database Schema](#database-schema)
- [How it Maps to Real Cloud](#how-it-maps-to-real-cloud)
- [Common Errors & Fixes](#common-errors--fixes)
- [Learning Outcomes](#learning-outcomes)

---

## What is this project?

This project is a **local simulation of a cloud-based event registration system**. Instead of deploying to a real cloud platform, every component runs on your own machine — but uses the same architecture patterns a production cloud app would use.

| Local Component | Simulates |
|---|---|
| Flask on port 5000 | Cloud Run / AWS Lambda |
| SQLite (`database.db`) | Firestore / AWS DynamoDB |
| HTML/JS served by Flask | Firebase Hosting / Vercel |
| `localhost:5000` URL | `https://yourapp.com` |

---

## Architecture Overview

```
Browser (User)
     │
     │  HTTP GET /          → Flask serves the registration form
     │  HTTP POST /register → Flask validates + saves to SQLite
     │  HTTP GET /registrations → Flask queries + returns table page
     │
     ▼
Flask API Server (app.py) — port 5000
     │
     ▼
SQLite Database (database.db)
  └── Table: registrations
        ├── id
        ├── name
        ├── email
        ├── event
        └── registered_at
```

### Request-Response Flow

```
1. User fills form → clicks Register
2. JavaScript fetch() sends POST /register with JSON body
3. Flask receives request → validates name + event
4. Flask inserts record into SQLite with timestamp
5. Flask returns {"message": "Registered successfully!"}
6. JavaScript shows success message in browser (no page reload)
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML, CSS, JavaScript | User interface & form submission |
| **Backend** | Python + Flask | HTTP server, API routes, business logic |
| **Database** | SQLite (`sqlite3`) | Persistent storage of registrations |
| **Fonts** | Google Fonts (Outfit, JetBrains Mono) | Visual styling |

---

## Project Structure

```
project/
│
├── app.py              # Main application — Flask server + all routes
├── database.db         # Auto-created on first run (do not edit manually)
└── README.md           # This file
```

> **Note:** There is no separate frontend file. The HTML is served directly by Flask from inside `app.py` — this is intentional and avoids CORS issues that occur when opening HTML files via `file://`.

---

## Setup & Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A terminal (Command Prompt on Windows, Terminal on Mac/Linux)

### Step 1 — Install Flask

```bash
pip install flask
```

> `flask-cors` is **not needed** because Flask serves the HTML itself — both frontend and backend share the same origin (`localhost:5000`).

### Step 2 — Download the project

Save `app.py` to a folder on your computer, for example:

```
C:\Users\YourName\Desktop\cloud-app\app.py
```

---

## Running the App

### Step 1 — Open Command Prompt

Press `Windows + R`, type `cmd`, press Enter.

### Step 2 — Navigate to your project folder

```bash
cd Desktop\cloud-app
```

### Step 3 — Run the Flask server

```bash
python app.py
```

You should see:

```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
* Press CTRL+C to quit
```

### Step 4 — Open the app in your browser

Visit: **[http://localhost:5000](http://localhost:5000)**

### Step 5 — Stop the server

Press `Ctrl + C` in the terminal.

---

## Pages & Routes

| Route | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the registration form (HTML page) |
| `/register` | `POST` | Receives form data, validates, saves to database |
| `/registrations` | `GET` | Shows all registrations as a formatted table |
| `/data` | `GET` | Returns all registrations as raw JSON (for debugging) |

### Example API calls

**Register a new person:**
```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Priya Sharma", "email": "priya@example.com", "event": "Cloud Workshop"}'
```

**Response:**
```json
{
  "message": "Registered successfully! Welcome, Priya Sharma."
}
```

**Get all registrations as JSON:**
```bash
curl http://localhost:5000/data
```

---

## Database Schema

The app automatically creates `database.db` and the `registrations` table on first run.

```sql
CREATE TABLE IF NOT EXISTS registrations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    email         TEXT,
    event         TEXT    NOT NULL,
    registered_at TEXT    NOT NULL
);
```

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Auto-increments — unique row identifier |
| `name` | TEXT | Full name of registrant (required) |
| `email` | TEXT | Email address (optional) |
| `event` | TEXT | Name of the event (required) |
| `registered_at` | TEXT | Timestamp: `YYYY-MM-DD HH:MM:SS` |

### Resetting the database

If you want to clear all data or fix a schema mismatch:

```bash
# Windows
del database.db

# Mac / Linux
rm database.db
```

Then restart `python app.py` — Flask will recreate the database automatically.

---

## How it Maps to Real Cloud

This project teaches the same concepts used in production cloud systems:

```
LOCAL                           CLOUD EQUIVALENT
─────────────────────────────────────────────────────────
python app.py                   Deploy container to Cloud Run
localhost:5000                  https://yourapp.com (HTTPS)
Flask routes                    Serverless functions (Lambda)
SQLite file                     Firestore / PostgreSQL
HTML served by Flask            Firebase Hosting / Vercel CDN
Terminal logs                   Cloud Logging / CloudWatch
Your PC's CPU/RAM               Cloud compute instances
Single user only                Auto-scales to millions
```

### Why not just use the cloud directly?

Cloud platforms require accounts, billing setup, and deployment pipelines. This local simulation lets you **learn and test the exact same architecture for free**, with instant feedback.

---

## Common Errors & Fixes

### ❌ `SyntaxError: invalid syntax` when running `cd` or `pip`

**Cause:** You're typing commands into the Python shell (`>>>`) instead of Command Prompt.

**Fix:** Type `exit()` to close Python, then open a fresh Command Prompt window.

---

### ❌ `ModuleNotFoundError: No module named 'flask'`

**Cause:** Flask is not installed.

**Fix:**
```bash
pip install flask
```

---

### ❌ `OperationalError: table registrations has no column named email`

**Cause:** You're using an old `database.db` created before the email column was added.

**Fix:**
```bash
del database.db   # Windows
python app.py     # Restart — fresh DB is created automatically
```

---

### ❌ `Address already in use` / port 5000 conflict

**Cause:** Another process is already using port 5000.

**Fix:** Stop the other process, or run Flask on a different port:
```bash
# In app.py, change the last line to:
app.run(debug=True, port=5001)
```

Then visit `http://localhost:5001`.

---

### ❌ `Cannot reach backend` error in browser

**Cause:** Flask is not running, or the HTML is being opened via `file://` instead of through Flask.

**Fix:** Always access the app via `http://localhost:5000` — never open `index.html` by double-clicking it.

---

## Learning Outcomes

By building and running this project, you learn:

1. **Client-Server Model** — How a browser communicates with a backend server using HTTP requests and responses.

2. **REST API Design** — How to structure routes using GET and POST methods, following patterns used in every modern cloud API.

3. **Database Persistence** — How structured data is stored, queried, and retrieved using SQL — the same concepts that apply to Firestore, DynamoDB, and Cloud SQL.

4. **CORS & Same-Origin Policy** — Why browsers block requests from `file://` to `localhost`, and how serving the frontend from Flask itself solves this.

5. **JSON Data Exchange** — How the frontend and backend communicate using JSON — the universal language of APIs.

6. **Full-Stack Integration** — How frontend, backend, and database connect into one cohesive system — the foundation of every cloud application.

---

## Author

**Project:** Local Cloud Simulation — Event Registration App  
**Purpose:** Academic submission demonstrating cloud computing principles  
**Stack:** Python · Flask · SQLite · HTML · JavaScript

---

> *"The best way to understand the cloud is to build it yourself — locally."*
