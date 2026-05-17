cat > README.md << 'README_EOF'
# AI Agent Learning Project

This is a personal learning project for building an SRE-style AI agent using Python, FastAPI, and Google Gemini.

The project demonstrates how an agent can call a monitoring API, analyze service health signals, classify severity, identify likely causes, and generate both deterministic and AI-assisted incident triage reports.

All services, metrics, incidents, and deployment details in this project are synthetic examples created for learning purposes.

---

## What This Project Demonstrates

This project demonstrates a simple but realistic agent-style architecture:

~~~text
Mock Monitoring API
        ↓
Monitoring Tool
        ↓
Incident Analyzer
        ↓
Gemini AI Explanation
        ↓
Human-readable report + structured JSON
~~~

The key learning idea is:

~~~text
Tools get facts.
Rules classify facts.
LLMs explain facts.
Agents orchestrate the workflow.
~~~

---

## Project Structure

~~~text
ai-agent-learning/
│
├── mock_monitoring_api/
│   └── main.py
│
├── sre_agent/
│   ├── __init__.py
│   ├── agent.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── incident_analyzer.py
│   │
│   └── tools/
│       ├── __init__.py
│       └── monitoring_tools.py
│
├── .env              # local only, not committed
├── .gitignore
├── README.md
└── requirements.txt
~~~

---

## Components

### 1. Mock Monitoring API

The mock monitoring API simulates a monitoring system such as CloudWatch, Datadog, Prometheus, or Grafana.

It exposes an endpoint like:

~~~text
GET /health/{service_name}
~~~

Example:

~~~text
GET /health/checkout
~~~

It returns synthetic service health data such as:

~~~json
{
  "service": "checkout",
  "status": "degraded",
  "availability": "99.72%",
  "latency_p95_ms": 1800,
  "error_rate_percent": 6.2,
  "recent_change": "Payment validation release deployed 45 minutes ago",
  "timestamp": 1779040056
}
~~~

### 2. Monitoring Tool

The monitoring tool lives in:

~~~text
sre_agent/tools/monitoring_tools.py
~~~

Its responsibility is to call the mock monitoring API and fetch service health data.

This is considered a "tool" because it reaches outside the agent to retrieve facts from an external system.

### 3. Incident Analyzer

The incident analyzer lives in:

~~~text
sre_agent/analysis/incident_analyzer.py
~~~

Its responsibility is to apply deterministic SRE rules:

- classify severity
- detect likely cause
- recommend action
- build structured incident analysis

This is internal reasoning logic, not an external tool.

### 4. SRE Agent Orchestrator

The main agent lives in:

~~~text
sre_agent/agent.py
~~~

Its responsibility is to orchestrate the workflow:

~~~text
1. Read service name from command line
2. Call monitoring tool
3. Build rule-based incident analysis
4. Ask Gemini for AI-generated explanation
5. Print human-readable report
6. Print structured JSON output
~~~

---

## Setup Instructions

### 1. Clone the repository

~~~bash
git clone https://github.com/venkateshvelaga/ai-agent-learning.git
cd ai-agent-learning
~~~

### 2. Create a virtual environment

~~~bash
python -m venv .venv
~~~

### 3. Activate the virtual environment

#### Git Bash

~~~bash
source .venv/Scripts/activate
~~~

#### PowerShell

~~~powershell
.venv\Scripts\activate
~~~

If PowerShell blocks script execution, run:

~~~powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
~~~

Then activate again:

~~~powershell
.venv\Scripts\activate
~~~

### 4. Install dependencies

~~~bash
pip install -r requirements.txt
~~~

---

## Environment Variables

This project uses a local `.env` file for secrets and configuration.

Create a `.env` file in the project root:

~~~bash
touch .env
~~~

Add your Gemini API key:

~~~env
GEMINI_API_KEY=your_actual_gemini_api_key_here
~~~

Optional monitoring API base URL:

~~~env
MONITORING_API_BASE_URL=http://127.0.0.1:8000
~~~

The `.env` file must never be committed.

Make sure `.gitignore` contains:

~~~text
.env
.venv/
__pycache__/
*.pyc
~~~

---

## Gemini API Key

This project uses Google Gemini for AI-generated incident explanation.

Get a Gemini API key from Google AI Studio:

~~~text
https://aistudio.google.com/app/apikey
~~~

For learning, create an API key in a new project.

The Python code loads the key from `.env` using:

~~~python
from dotenv import load_dotenv
load_dotenv()
~~~

Then it reads:

~~~python
os.getenv("GEMINI_API_KEY")
~~~

---

## Running the Project

You need two terminal windows.

---

### Terminal 1: Start the Mock Monitoring API

~~~bash
cd ai-agent-learning
source .venv/Scripts/activate
uvicorn mock_monitoring_api.main:app --reload
~~~

The API will run at:

~~~text
http://127.0.0.1:8000
~~~

Open the health endpoint in a browser:

~~~text
http://127.0.0.1:8000/health/checkout
~~~

Open FastAPI Swagger docs:

~~~text
http://127.0.0.1:8000/docs
~~~

---

### Terminal 2: Run the SRE Agent

Because the project now uses Python package-style imports, run the agent as a module:

~~~bash
cd ai-agent-learning
source .venv/Scripts/activate
python -m sre_agent.agent checkout
~~~

You can test different service names:

~~~bash
python -m sre_agent.agent checkout
python -m sre_agent.agent payment
python -m sre_agent.agent order
~~~

Do not run it like this anymore:

~~~bash
python sre_agent/agent.py checkout
~~~

The module command is preferred because `sre_agent` is now a package.

---

## Example Agent Output

~~~text
================ SRE INCIDENT TRIAGE REPORT ================

Service: checkout
Status: HEALTHY
Severity: SEV-4

Evidence:
- Availability: 99.99%
- P95 latency: 183 ms
- Error rate: 0.73%
- Recent change: No risky deployment detected

Likely cause:
No obvious cause detected from current signals.

Recommended action:
No immediate action required.

Leadership summary:
checkout is currently healthy with severity SEV-4. Main signals: availability 99.99%, p95 latency 183 ms, error rate 0.73%.

AI-generated incident explanation:
## Incident Explanation: Checkout Service

1. What is happening

The checkout service is currently reporting as healthy. Availability is at 99.99%, P95 latency is 183 ms, and the error rate is 0.73%.

2. Why this is likely happening

Based on the provided data, there are no immediate indicators of an issue. All monitored metrics are within acceptable healthy ranges.

3. Immediate next actions

No immediate actions are required. Continue to monitor the checkout service for any changes in health metrics.

4. Leadership update

The checkout service is currently healthy with severity SEV-4.

============================================================

Structured JSON output:
{
  "service": "checkout",
  "status": "healthy",
  "severity": "SEV-4",
  "evidence": {
    "availability": "99.99%",
    "latency_p95_ms": 183,
    "error_rate_percent": 0.73,
    "recent_change": "No risky deployment detected"
  },
  "likely_cause": "No obvious cause detected from current signals.",
  "recommended_action": "No immediate action required.",
  "leadership_summary": "checkout is currently healthy with severity SEV-4. Main signals: availability 99.99%, p95 latency 183 ms, error rate 0.73%."
}
~~~

---

## Severity Rules

The current rule-based analyzer uses simple severity logic:

| Severity | Condition |
|---|---|
| SEV-1 | Availability < 99.5% or error rate >= 7.0% |
| SEV-2 | P95 latency >= 1500 ms or error rate >= 5.0% |
| SEV-3 | Degraded but below SEV-1/SEV-2 thresholds |
| SEV-4 | Healthy |

---

## Why Use Rules and Gemini Together?

The project intentionally uses both deterministic rules and an LLM.

Rules are used for:

- severity classification
- threshold-based decisions
- repeatable logic
- structured incident fields

Gemini is used for:

- incident explanation
- leadership-friendly summary
- natural language reasoning
- recommended next-step wording

The pattern is:

~~~text
Rules decide the facts.
Gemini explains the facts.
~~~

This is safer than letting the LLM invent severity or make uncontrolled operational decisions.

---

## Error Handling

The monitoring tool handles common failures gracefully:

- monitoring API is not running
- request timeout
- HTTP errors
- invalid JSON response
- general request failure

Example:

~~~text
ERROR: Could not connect to mock monitoring API.
Make sure it is running with:
uvicorn mock_monitoring_api.main:app --reload
~~~

The Gemini explanation function also handles AI call failures gracefully.

If Gemini fails, the agent still prints the deterministic rule-based incident report.

---

## Learning Goals

This project is intended to teach:

- Python project setup
- virtual environments
- FastAPI basics
- REST API calls
- command-line Python modules
- JSON handling
- environment variables
- safe API key handling
- rule-based agent logic
- SRE incident triage concepts
- severity classification
- Gemini API integration
- LLM-assisted explanation
- tool-style agent architecture
- Python package imports
- Git/GitHub workflow

---

## Current Architecture

~~~text
User runs:
python -m sre_agent.agent checkout
      |
      v
sre_agent/agent.py
      |
      v
sre_agent/tools/monitoring_tools.py
      |
      v
GET http://127.0.0.1:8000/health/{service_name}
      |
      v
mock_monitoring_api/main.py
      |
      v
Synthetic health JSON
      |
      v
sre_agent/analysis/incident_analyzer.py
      |
      v
Rule-based incident analysis
      |
      v
Gemini API
      |
      v
AI-generated explanation
      |
      v
Incident triage report + structured JSON
~~~

---

## Git Safety

Files that should be committed:

~~~text
README.md
requirements.txt
.gitignore
mock_monitoring_api/main.py
sre_agent/agent.py
sre_agent/__init__.py
sre_agent/tools/monitoring_tools.py
sre_agent/tools/__init__.py
sre_agent/analysis/incident_analyzer.py
sre_agent/analysis/__init__.py
~~~

Files that should not be committed:

~~~text
.env
.venv/
__pycache__/
*.pyc
~~~

Before every commit, check:

~~~bash
git status
~~~

Make sure `.env` is not listed.

---

## Next Planned Enhancements

Possible next steps:

- Add real Google ADK agent structure
- Add multi-service health checks
- Add incident history
- Add Slack-style incident summary
- Add automated runbook recommendation
- Add unit tests
- Add Docker support
- Add GitHub Actions CI
- Add a small UI for triggering analysis

---

## Disclaimer

This is a personal learning project. It does not contain proprietary company code, internal service names, real production data, credentials, or confidential architecture details.
README_EOF