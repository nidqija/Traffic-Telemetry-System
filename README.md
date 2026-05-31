# Traffic Telemetry System 🚥
 
A dual-layer monitoring workspace that bridges embedded microcontroller traffic control firmware with a real-time analytics dashboard — no heavy infrastructure required.
 
---
 
## Overview
 
traffictelemetry connects two independent systems:
 
- **Hardware Layer** — An Arduino/ESP32 firmware sketch that drives physical LED signal nodes across dedicated digital pins with microsecond-accurate state cycling.
- **Software Layer** — A lightweight Streamlit + SQLite telemetry dashboard that acts as an analytical twin, logging operations, task states, and system overrides locally without any server setup.
---
 
## Architecture
 
```
┌─────────────────────────┐        ┌──────────────────────────────┐
│   Hardware (Firmware)   │        │   Software (Telemetry UI)    │
│                         │        │                              │
│  Arduino / ESP32        │        │  Streamlit frontend          │
│  C++ / Arduino FW       │        │  SQLite (local_app.db)       │
│  Digital pin cycling    │        │  Pandas DataFrames           │
│  Microsecond accuracy   │        │  Reactive split-screen UI    │
└─────────────────────────┘        └──────────────────────────────┘
         ↕ Independent execution — hardware never blocks the dashboard
```
 
---
 
## Features
 
**Hardware**
- Production-ready firmware loop that maps output signals cleanly across terminal pins
- Executes independently of the web layer — no analytical bottlenecks freeze active signal hardware
**Software**
- Zero-config database boot — `local_app.db` is provisioned automatically on first launch if it doesn't exist
- Reactive split-screen UI with isolated config inputs (left panel) and a live data grid (right panel)
- Thread-safe database operations using short-lived `sqlite3.connect` context closures, eliminating file lock conflicts
- SQL results piped directly into Pandas DataFrames for clean, scannable telemetry visualization
- SQL injection prevention via parameterized query syntax (`?` placeholders — no string interpolation)
- Optimized form controls via `st.form` to prevent full-page re-renders on every keystroke
---
 
## Repository Structure
 
```
.
├── src/
│   └── main.cpp        # Embedded C++ firmware — pin logic and signal state cycles
├── app.py              # Streamlit app — UI layout, form controls, and SQL operations
├── README.md           # Project documentation
└── local_app.db        # SQLite database (auto-generated on first run)
```
 
---
 
## Database Schema
 
A single table tracks all telemetry tasks and overrides:
 
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT    NOT NULL,
    category TEXT,
    status   TEXT    DEFAULT 'Pending'
);
```
 
---
 
## Tech Stack
 
| Layer      | Technology                        |
|------------|-----------------------------------|
| MCU Target | Arduino / ESP32                   |
| Firmware   | C++ / Arduino Framework           |
| Frontend   | Streamlit                         |
| Database   | SQLite (Python standard library)  |
| Data Layer | Pandas                            |
 
---
 
## Quick Start
 
### 1. Flash the Firmware
 
Open the project in VS Code with the [PlatformIO](https://platformio.org/) extension installed.
 
Use the PlatformIO status bar to:
- **Build** — click the ✓ checkmark
- **Upload** — click the → arrow to flash directly to your connected board
### 2. Run the Dashboard
 
Install Python dependencies:
 
```bash
pip install streamlit pandas
```
 
Launch the telemetry server:
 
```bash
streamlit run app.py
```
 
The dashboard opens automatically in your browser at `http://localhost:8501`. The database file `local_app.db` is created on first boot if it doesn't already exist.
 
---
 
## Design Decisions
 
| Decision | Rationale |
|----------|-----------|
| Hardware/software separation | Firmware cycles run independently — UI lag never interrupts active signal control |
| SQLite over a hosted DB | Zero infrastructure overhead; fully portable and self-contained |
| `st.form` for input controls | Prevents expensive full-page re-renders on every keypress in Streamlit |
| Parameterized SQL queries | Eliminates SQL injection risk without any additional libraries |
| `with sqlite3.connect(...)` | Short-lived connections prevent concurrent file lock conflicts |
