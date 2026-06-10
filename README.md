# Traffic Light Monitoring System 🚥
 
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-3498DB?style=for-the-badge&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare_Workers-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)

An integrated traffic monitoring system that combines embedded hardware control with AI-powered analytics. Bridges Arduino firmware with a Streamlit dashboard, powered by local Ollama LLM intelligence and Cloudflare Workers edge computing — all without expensive cloud infrastructure.
 
---
 
## Overview
 
Traffic Light Monitoring System connects three independent layers:
 
- **Hardware Layer** — Arduino/ESP32 firmware driving physical LED signal nodes with microsecond-accurate state cycling.
- **Dashboard Layer** — Streamlit frontend for real-time telemetry, traffic data visualization, and system control.
- **AI Intelligence Layer** — Ollama local LLM integration + Cloudflare Workers for natural language queries, pattern analysis, and intelligent traffic insights without external API calls.
---
 
## Architecture
 
```
┌──────────────────────┐   ┌──────────────────────────┐   ┌─────────────────────┐
│ Hardware (Arduino)   │   │  Dashboard (Streamlit)   │   │  AI Intelligence    │
│                      │   │                          │   │                     │
│ ESP32/Arduino        │   │ Web UI + Traffic Data    │   │ Ollama LLM          │
│ LED Signal Control   │   │ SQLite Data Store        │   │ (Local)             │
│ Real-time Cycling    │   │ Live Visualization      │   │                     │
└──────────────────────┘   └──────────────────────────┘   │ Cloudflare Workers  │
         ↕                           ↕                      │ (Edge Processing)   │
    [Independent]           [Query & Control]              └─────────────────────┘
                                                                    ↕
                                                        [AI Query Analysis]
                                                        [Pattern Detection]
                                                        [Natural Language]
```
 
---
 
## Features
 
**Hardware**
- Production-ready firmware loop that maps output signals cleanly across terminal pins
- Executes independently of the web layer — no analytical bottlenecks freeze active signal hardware

**Dashboard & Data**
- Real-time traffic telemetry dashboard with live data visualization
- Zero-config database boot — auto-provisioned SQLite on first launch
- Thread-safe database operations using short-lived connection contexts
- SQL results piped into Pandas DataFrames for clean telemetry visualization
- SQL injection prevention via parameterized query syntax
- Optimized form controls to prevent full-page re-renders

**AI & Intelligence**
- **Ollama Integration** — Local LLM deployment for traffic analysis without external API calls
- **Factory Pattern** — Pluggable AI backends (Ollama + Cloudflare Workers support)
- **Natural Language Queries** — Ask questions about traffic patterns in plain English
- **Smart Analytics** — AI-powered insights on traffic flow, congestion patterns, and optimization
- **Edge Processing** — Cloudflare Workers for low-latency AI query processing
---
 
## Repository Structure
 
```
.
├── arduino_snippet/
│   └── arduino_sketch/
│       └── arduino_sketch.ino        # ESP32/Arduino firmware
├── web_project/
│   ├── main.py                       # Application entry point
│   ├── home_page.py                  # Dashboard UI
│   ├── aiagent_query_dashboard.py    # AI query interface
│   ├── traffic_data.py               # Traffic telemetry module
│   ├── sqlite_script.py              # Database utilities
│   ├── ai_factory/
│   │   ├── base_factory.py           # Abstract AI factory
│   │   ├── ollama_factory.py         # Ollama LLM integration
│   │   ├── cloudflare_worker_factory.py  # Cloudflare Workers integration
│   │   └── factory_manager.py        # Factory orchestration
│   └── unit_test/
│       └── loop_list_of_arrays.py    # Test utilities
├── README.md
└── local_app.db                      # SQLite database (auto-generated)
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
 
| Layer           | Technology                        |
|-----------------|-----------------------------------|
| MCU Target      | Arduino / ESP32                   |
| Firmware        | C++ / Arduino Framework           |
| Frontend        | Streamlit                         |
| Backend         | Python                            |
| Database        | SQLite                            |
| Data Processing | Pandas                            |
| AI Engine       | Ollama (Local LLM)                |
| AI Factory      | Base Factory Pattern              |
| Edge Computing  | Cloudflare Workers                |
 
---
 
## Quick Start
 
### Prerequisites
- Python 3.8+
- Arduino IDE or PlatformIO
- Ollama (for local LLM features)
- Cloudflare account (optional, for edge processing)

### 1. Flash the Firmware
 
Open the project in VS Code with the [PlatformIO](https://platformio.org/) extension installed.
 
Use the PlatformIO status bar to:
- **Build** — click the ✓ checkmark
- **Upload** — click the → arrow to flash directly to your connected board

### 2. Set Up Ollama (Optional but Recommended)
 
Install [Ollama](https://ollama.ai/) on your system, then pull a model:
 
```bash
ollama pull llama2
# or use another model: mistral, neural-chat, etc.
ollama serve
```
 
This runs the Ollama server locally on `http://localhost:11434`. The AI factory will detect it automatically.

### 3. Install Python Dependencies
 
```bash
cd web_project
pip install streamlit pandas
```

### 4. Configure Cloudflare Workers (Optional)
 
If using Cloudflare Workers for edge AI processing:
 
1. Install [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
2. Create a `wrangler.toml` in the project root
3. Deploy your worker script

### 5. Run the Dashboard
 
Launch the Streamlit app:
 
```bash
streamlit run main.py
```
 
The dashboard opens at `http://localhost:8501`. Use the AI Query Dashboard tab to ask natural language questions about traffic patterns.
 
---
 
## AI Factory Pattern
 
The system uses a pluggable AI factory pattern to support multiple LLM backends:
 
- **Base Factory** (`base_factory.py`) — Abstract interface for all AI backends
- **Ollama Factory** (`ollama_factory.py`) — Local LLM processing (no external calls)
- **Cloudflare Workers Factory** (`cloudflare_worker_factory.py`) — Edge-based AI processing
 
### Using the AI Factory
 
```python
from ai_factory.factory_manager import FactoryManager

# Initialize factory manager
manager = FactoryManager()

# Query with automatic backend selection
response = manager.query("What traffic patterns occurred between 2-3 PM?")
```
 
The factory manager automatically selects the best backend based on availability and configuration.

---

## Configuration
 
### Environment Variables
 
Create a `.env` file in the `web_project/` directory:
 
```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# Cloudflare Configuration (optional)
CLOUDFLARE_API_TOKEN=your_token_here
CLOUDFLARE_ACCOUNT_ID=your_account_id_here
CLOUDFLARE_WORKER_URL=https://your-worker.workers.dev

# Database
DB_PATH=./local_app.db

# AI Factory (default: ollama)
AI_FACTORY_TYPE=ollama  # or cloudflare
```

### Database Schema
 
The system automatically initializes the traffic data table on first run:
 
```sql
CREATE TABLE IF NOT EXISTS traffic_data (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    signal_state TEXT,
    vehicle_count INTEGER,
    average_wait_time REAL,
    status TEXT DEFAULT 'Active'
);
```

---

## Troubleshooting
 
| Issue | Solution |
|-------|----------|
| Ollama connection fails | Ensure Ollama is running: `ollama serve` |
| "Model not found" error | Pull a model: `ollama pull llama2` |
| Streamlit crashes on startup | Install missing dependencies: `pip install -r requirements.txt` |
| SQLite database locked | Close all other connections and restart the app |
| Arduino upload fails | Select the correct port and board in PlatformIO settings |

---

## Design Decisions
 
| Decision | Rationale |
|----------|-----------|
| Hardware/software separation | Firmware cycles run independently — UI lag never interrupts active signal control |
| SQLite over a hosted DB | Zero infrastructure overhead; fully portable and self-contained |
| Factory Pattern for AI | Enables flexible backend switching (Ollama ↔ Cloudflare) without code changes |
| Ollama as default AI | Local LLM deployment ensures privacy and reduces API costs |
| `st.form` for input controls | Prevents expensive full-page re-renders on every keypress in Streamlit |
| Parameterized SQL queries | Eliminates SQL injection risk without any additional libraries |
| `with sqlite3.connect(...)` | Short-lived connections prevent concurrent file lock conflicts |

---

## License

MIT License — See LICENSE file for details
