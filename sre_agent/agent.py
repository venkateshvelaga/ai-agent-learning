import sys
import requests


def get_service_health(service_name: str):
    url = f"http://127.0.0.1:8000/health/{service_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def classify_severity(health_data: dict):
    status = health_data["status"]
    latency = health_data["latency_p95_ms"]
    error_rate = health_data["error_rate_percent"]
    availability = float(health_data["availability"].replace("%", ""))

    if status == "healthy":
        return "SEV-4"

    if availability < 99.5 or error_rate >= 7.0:
        return "SEV-1"

    if latency >= 1500 or error_rate >= 5.0:
        return "SEV-2"

    return "SEV-3"


def find_likely_cause(health_data: dict):
    recent_change = health_data["recent_change"].lower()

    if "deployed" in recent_change or "release" in recent_change:
        return "Recent deployment is a likely contributor."

    if health_data["latency_p95_ms"] > 1000:
        return "High latency suggests a downstream dependency or performance bottleneck."

    if health_data["error_rate_percent"] > 4:
        return "Elevated errors suggest service instability or dependency failures."

    return "No obvious cause detected from current signals."


def recommend_action(severity: str):
    if severity == "SEV-1":
        return "Page on-call immediately, start incident bridge, check rollback readiness."
    if severity == "SEV-2":
        return "Notify service owner, investigate recent changes, validate dependency health."
    if severity == "SEV-3":
        return "Monitor closely and review logs/metrics for trend confirmation."
    return "No immediate action required."


def analyze_health(health_data: dict):
    severity = classify_severity(health_data)
    likely_cause = find_likely_cause(health_data)
    action = recommend_action(severity)

    return f"""
================ SRE INCIDENT TRIAGE REPORT ================

Service: {health_data["service"]}
Status: {health_data["status"].upper()}
Severity: {severity}

Evidence:
- Availability: {health_data["availability"]}
- P95 latency: {health_data["latency_p95_ms"]} ms
- Error rate: {health_data["error_rate_percent"]}%
- Recent change: {health_data["recent_change"]}

Likely cause:
{likely_cause}

Recommended action:
{action}

Leadership summary:
{health_data["service"]} is currently {health_data["status"]} with severity {severity}. The main signals are availability {health_data["availability"]}, p95 latency {health_data["latency_p95_ms"]} ms, and error rate {health_data["error_rate_percent"]}%.

============================================================
"""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sre_agent/agent.py <service_name>")
        print("Example: python sre_agent/agent.py checkout")
        sys.exit(1)

    service_name = sys.argv[1]
    health = get_service_health(service_name)
    analysis = analyze_health(health)
    print(analysis)