# 🧠 Kumo FinOps Engine - Backend API

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)

The intelligence core of the **Kumo Platform**. This high-performance API handles data ingestion, performs statistical anomaly detection using Z-Score algorithms, and dispatches real-time alerts to Slack.

---

## 🏗️ System Architecture

This backend serves as the logic layer between the User Interface and the Database.

```mermaid
graph LR
    A[Next.js Frontend] -->|POST /ingest| B(FastAPI Engine)
    B -->|Store Data| C[(PostgreSQL)]
    B -->|Calculate Z-Score| D{Anomaly?}
    D -- Yes --> E[Slack Webhook]
    D -- No --> F[Return Normal Status]
```

_(Note: The diagram above renders automatically on GitHub)_

---
### 🚀 Demo: 

https://github.com/user-attachments/assets/a84c2c59-8416-4fdb-85e9-8188bb657cf8




## 🧮 The Logic: Z-Score Algorithm

To detect spending spikes, Kumo uses a statistical approach rather than fixed thresholds. This allows it to adapt to different spending baselines.

**Formula:**
$$Z = \frac{(X - \mu)}{\sigma}$$

- **$X$**: Current transaction amount.
- **$\mu$ (Mu)**: Moving average of historical costs.
- **$\sigma$ (Sigma)**: Standard deviation (volatility) of costs.

> **Decision Rule:** If the Z-Score is greater than **3** (i.e., the cost is 3 standard deviations away from the mean), it is flagged as an **Anomaly**.

---

## 🚀 Quick Start (Local)

### Option 1: Using Docker (Recommended)

You can spin up the API and Database instantly using Docker Compose.

```bash
# 1. Clone the repo
git clone [https://github.com/hitanshu04/kumo-finops-engine.git](https://github.com/hitanshu04/kumo-finops-engine.git)

# 2. Start Services
docker-compose up -d --build
```

The API will be live at: **http://localhost:8000**

### Option 2: Manual Setup

If you don't have Docker, run it with Python directly.

```bash
# 1. Create Virtual Env
python -m venv venv

# Activate Virtual Env (Windows)
venv\Scripts\activate
# OR for Mac/Linux: source venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Setup Database
# Ensure your Postgres is running and update .env file

# 4. Run Server
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

Once running, visit the **Interactive Swagger Documentation** at:  
👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

| Method | Endpoint   | Description                                                            |
| :----- | :--------- | :--------------------------------------------------------------------- |
| `GET`  | `/`        | Health Check (Returns "Ready for Money")                               |
| `POST` | `/ingest/` | **Main Engine:** Accepts cost data, saves to DB, checks for anomalies. |
| `GET`  | `/costs/`  | Retrieves history of cost entries for charts.                          |

---

## 📂 Project Structure

```bash
kumo-engine/
├── app/
│   ├── main.py           # Entry point, CORS settings, API routes
│   ├── models.py         # SQLAlchemy Database Models
│   ├── schemas.py        # Pydantic Data Validation
│   ├── crud.py           # Database Logic (Create/Read)
│   └── database.py       # DB Connection Setup
├── Dockerfile            # Container instructions
├── docker-compose.yml    # Orchestration for API + DB
├── requirements.txt      # Python dependencies
└── .env.example          # Environment variables template
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
# Database Connection String
DB_URL=postgresql://user:password@localhost:5432/kumo

# Optional: Slack Webhook (If configured in backend directly)
SLACK_WEBHOOK_URL=[https://hooks.slack.com/services/YOUR/WEBHOOK/URL](https://hooks.slack.com/services/YOUR/WEBHOOK/URL)
```

---

---

## 🔗 Project Links

Looking for the Frontend Dashboard?  
👉 **[View Frontend Repository (Next.js UI)](https://github.com/hitanshu04/kumo-frontend)**

_Backend Architected with ❤️ by Hitanshu Kumar Singh_
