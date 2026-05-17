# AI Agent Learning Project

This is a personal learning project for building an SRE-style AI agent using Python.

The project demonstrates how an agent can call a monitoring API, analyze service health signals, classify severity, identify likely causes, and generate an incident-style triage report.

All services, metrics, incidents, and deployment details in this project are synthetic examples created for learning purposes.

---

## Project Structure

~~~text
ai-agent-learning/
│
├── mock_monitoring_api/
│   └── main.py
│
├── sre_agent/
│   ├── .gitkeep
│   └── agent.py
│
├── .gitignore
├── README.md
└── requirements.txt
~~~

---

## What This Project Does

The project has two main parts:

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

### 2. SRE Agent

The SRE agent calls the mock monitoring API and produces:

- service status
- severity classification
- evidence
- likely cause
- recommended action
- leadership summary
- structured JSON output

Example command:

~~~bash
python sre_agent/agent.py checkout
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

~~~bash
cd ai-agent-learning
source .venv/Scripts/activate
python sre_agent/agent.py checkout
~~~

You can test different service names:

~~~bash
python sre_agent/agent.py checkout
python sre_agent/agent.py payment
python sre_agent/agent.py order
~~~

---

## Environment Configuration

By default, the agent calls:

~~~text
http://127.0.0.1:8000
~~~

You can override the monitoring API base URL using an environment variable.

### Git Bash

~~~bash
MONITORING_API_BASE_URL=http://127.0.0.1:8000 python sre_agent/agent.py checkout
~~~

### PowerShell

~~~powershell
$env:MONITORING_API_BASE_URL="http://127.0.0.1:8000"
python sre_agent/agent.py checkout
~~~

---

## Example Agent Output

~~~text
================ SRE INCIDENT TRIAGE REPORT ================

Service: checkout
Status: DEGRADED
Severity: SEV-2

Evidence:
- Availability: 99.72%
- P95 latency: 2161 ms
- Error rate: 4.53%
- Recent change: Payment validation release deployed 45 minutes ago

Likely cause:
Recent deployment is a likely contributor.

Recommended action:
Notify service owner, investigate recent changes, validate dependency health.

Leadership summary:
checkout is currently degraded with severity SEV-2. Main signals: availability 99.72%, p95 latency 2161 ms, error rate 4.53%.

============================================================

Structured JSON output:
{
  "service": "checkout",
  "status": "degraded",
  "severity": "SEV-2",
  "evidence": {
    "availability": "99.72%",
    "latency_p95_ms": 2161,
    "error_rate_percent": 4.53,
    "recent_change": "Payment validation release deployed 45 minutes ago"
  },
  "likely_cause": "Recent deployment is a likely contributor.",
  "recommended_action": "Notify service owner, investigate recent changes, validate dependency health.",
  "leadership_summary": "checkout is currently degraded with severity SEV-2. Main signals: availability 99.72%, p95 latency 2161 ms, error rate 4.53%."
}
~~~

---

## Severity Rules

The current rule-based agent uses simple severity logic:

| Severity | Condition |
|---|---|
| SEV-1 | Availability < 99.5% or error rate >= 7.0% |
| SEV-2 | P95 latency >= 1500 ms or error rate >= 5.0% |
| SEV-3 | Degraded but below SEV-1/SEV-2 thresholds |
| SEV-4 | Healthy |

---

## Error Handling

The agent handles common failures gracefully:

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

---

## Learning Goals

This project is intended to teach:

- Python project setup
- virtual environments
- FastAPI basics
- REST API calls
- command-line Python scripts
- JSON handling
- rule-based agent logic
- SRE incident triage concepts
- severity classification
- Git/GitHub workflow
- preparing for LLM-powered agents

---

## Current Architecture

~~~text
User runs agent
      |
      v
sre_agent/agent.py
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
Agent severity/cause/action logic
      |
      v
Incident triage report + structured JSON
~~~

---

## Next Planned Enhancements

Possible next steps:

- Add LLM/Gemini-based incident explanation
- Add Google ADK-style tool calling
- Add multi-service health checks
- Add incident history
- Add Slack-style incident summary
- Add automated runbook recommendation
- Add tests
- Add Docker support

---

## Disclaimer

This is a personal learning project. It does not contain proprietary company code, internal service names, real production data, credentials, or confidential architecture details.
