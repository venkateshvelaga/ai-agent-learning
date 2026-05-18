# AI Agent Learning Project

This is a personal learning project for building an SRE-style AI agent using Python, FastAPI, Google Gemini, and MCP.

The project demonstrates how an agent can call a monitoring API, analyze service health signals, classify severity, identify likely causes, and generate both deterministic and AI-assisted incident triage reports.

All services, metrics, incidents, and deployment details in this project are synthetic examples created for learning purposes.

---

## What This Project Demonstrates

This project demonstrates a simple but realistic agent-style architecture with two ways of interacting with tools:

1. Direct Python tool call
2. MCP-based tool call

The key learning idea is:

~~~text
Tools get facts.
Rules classify facts.
LLMs explain facts.
Agents orchestrate the workflow.
MCP standardizes how agents call tools.
~~~

---

## Two Interaction Modes

This project supports two ways to run the SRE agent.

---

### Mode 1: Direct Python Tool Agent

In this mode, the agent directly imports and calls the Python monitoring tool.

~~~text
Direct Agent
      ↓
monitoring_tools.get_service_health()
      ↓
Mock Monitoring API
      ↓
Incident Analyzer
      ↓
Gemini Explanation
      ↓
Incident Report
~~~

Run with:

~~~bash
python -m sre_agent.agent checkout
~~~

This mode is simpler and easier to understand first.

---

### Mode 2: MCP-Based Agent

In this mode, the agent does not call the monitoring tool directly.

Instead, it acts as an MCP client. The MCP client starts/connects to an MCP server. The MCP server exposes the monitoring function as a tool.

~~~text
MCP Agent
      ↓
MCP Client
      ↓
MCP Server
      ↓
MCP Tool: get_service_health_tool()
      ↓
monitoring_tools.get_service_health()
      ↓
Mock Monitoring API
      ↓
Incident Analyzer
      ↓
Gemini Explanation
      ↓
Incident Report
~~~

Run with:

~~~bash
python -m sre_agent.agent_mcp checkout
~~~

This mode is closer to how tools can be exposed through a standard protocol and reused by different AI clients.

---

## Direct Tool vs MCP Tool

| Area | Direct Python Tool Agent | MCP-Based Agent |
|---|---|---|
| Command | `python -m sre_agent.agent checkout` | `python -m sre_agent.agent_mcp checkout` |
| Tool call style | Direct Python import/function call | MCP client/server tool call |
| Simplicity | Simpler | More realistic integration pattern |
| Tool discovery | Not needed | MCP supports tool discovery |
| Reusability | Mostly this app | MCP tools can be reused by MCP-compatible clients |
| Best for | Learning basic agent flow | Learning standardized tool integration |

---

## Current Architecture

~~~text
ai-agent-learning/
│
├── mock_monitoring_api/
│   └── main.py
│
├── sre_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent_mcp.py
│   ├── mcp_client_test.py
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   └── gemini_explainer.py
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── incident_analyzer.py
│   │
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   └── server.py
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   └── report_formatter.py
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

This is the actual implementation used by both the direct agent and the MCP server.

### 3. MCP Server

The MCP server lives in:

~~~text
sre_agent/mcp_server/server.py
~~~

It exposes the monitoring function as an MCP tool:

~~~text
get_service_health_tool(service_name)
~~~

The MCP server is not the agent. It is a tool provider.

### 4. MCP Client Test

The MCP client test lives in:

~~~text
sre_agent/mcp_client_test.py
~~~

It verifies that the MCP server can:

- start successfully
- list available tools
- call `get_service_health_tool`
- return health data

Run with:

~~~bash
python -m sre_agent.mcp_client_test
~~~

### 5. Incident Analyzer

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

### 6. Gemini Explainer

The Gemini explainer lives in:

~~~text
sre_agent/ai/gemini_explainer.py
~~~

Its responsibility is to call Gemini and generate a human-readable incident explanation based on:

- service health data
- rule-based incident analysis

### 7. Report Formatter

The report formatter lives in:

~~~text
sre_agent/reporting/report_formatter.py
~~~

Its responsibility is to format the final incident triage report.

Both the direct agent and MCP-based agent reuse this module.

### 8. Agent Entrypoints

There are two agent entrypoints:

~~~text
sre_agent/agent.py       # Direct Python tool agent
sre_agent/agent_mcp.py   # MCP-based agent
~~~

Both produce similar incident reports, but they fetch service health differently.

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

You need at least two terminal windows.

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

### Terminal 2 Option A: Run Direct Python Tool Agent

~~~bash
cd ai-agent-learning
source .venv/Scripts/activate
python -m sre_agent.agent checkout
~~~

Try different services:

~~~bash
python -m sre_agent.agent checkout
python -m sre_agent.agent payment
python -m sre_agent.agent order
~~~

---

### Terminal 2 Option B: Run MCP-Based Agent

~~~bash
cd ai-agent-learning
source .venv/Scripts/activate
python -m sre_agent.agent_mcp checkout
~~~

Try different services:

~~~bash
python -m sre_agent.agent_mcp checkout
python -m sre_agent.agent_mcp payment
python -m sre_agent.agent_mcp order
~~~

The MCP-based agent starts the MCP server through stdio using:

~~~bash
python -m sre_agent.mcp_server.server
~~~

You do not need to manually start the MCP server in a separate terminal for this local stdio setup.

---

### Optional: Test MCP Server Directly

~~~bash
python -m sre_agent.mcp_client_test
~~~

This lists MCP tools and calls the MCP health tool directly.

---

## Example Agent Output

~~~text
================ SRE INCIDENT TRIAGE REPORT ================

Execution mode: MCP-based agent

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

## Why Add MCP?

MCP adds a standard tool-provider layer.

Without MCP:

~~~text
Agent directly imports and calls Python functions.
~~~

With MCP:

~~~text
Agent calls tools through an MCP client/server protocol.
~~~

This matters because MCP tools can be reused by different MCP-compatible clients and agents.

In this project:

~~~text
MCP server = tool provider
MCP client = code inside agent_mcp.py
MCP tool = get_service_health_tool
Actual implementation = monitoring_tools.get_service_health
External system = mock monitoring API
~~~

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
- MCP server basics
- MCP client basics
- Python package imports
- Git/GitHub workflow

---

## Git Safety

Files that should be committed:

~~~text
README.md
requirements.txt
.gitignore
mock_monitoring_api/main.py
sre_agent/agent.py
sre_agent/agent_mcp.py
sre_agent/mcp_client_test.py
sre_agent/__init__.py
sre_agent/ai/gemini_explainer.py
sre_agent/ai/__init__.py
sre_agent/tools/monitoring_tools.py
sre_agent/tools/__init__.py
sre_agent/analysis/incident_analyzer.py
sre_agent/analysis/__init__.py
sre_agent/mcp_server/server.py
sre_agent/mcp_server/__init__.py
sre_agent/reporting/report_formatter.py
sre_agent/reporting/__init__.py
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

## Recommended Next Enhancements

Recommended learning order:

1. Add multi-service health checks
   - Support commands like:
     `python -m sre_agent.agent_mcp checkout payment order`
   - Rank services by severity.
   - Generate an overall incident summary.

2. Add automated runbook recommendation
   - Add local runbook files.
   - Recommend the best runbook based on severity, latency, errors, and recent changes.

3. Add incident history
   - Store past incident analyses locally.
   - Compare current incidents with previous patterns.

4. Add Slack-style incident summary
   - Generate short updates suitable for incident channels and leadership updates.

5. Add unit tests
   - Test severity classification, cause detection, runbook selection, and multi-service ranking.

6. Add Docker support
   - Containerize the mock monitoring API and agent.

7. Add GitHub Actions CI
   - Run tests automatically on every push.

8. Convert the current ADK-style Python agent into a Google ADK-based agent
   - Register tools with an actual ADK agent.
   - Use ADK runner/session concepts.
   - Compare ADK tool calling with MCP tool calling.

9. Add a small UI for triggering analysis
   - Add a simple local web UI or Streamlit-style interface.

---

## Disclaimer

This is a personal learning project. It does not contain proprietary company code, internal service names, real production data, credentials, or confidential architecture details.
