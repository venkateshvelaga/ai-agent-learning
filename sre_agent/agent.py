import sys
import requests


def get_service_health(service_name: str):
    url = f"http://127.0.0.1:8000/health/{service_name}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def analyze_health(health_data: dict):
    status = health_data["status"]

    if status == "healthy":
        return f"""
Service: {health_data["service"]}
Status: HEALTHY

Availability: {health_data["availability"]}
P95 latency: {health_data["latency_p95_ms"]} ms
Error rate: {health_data["error_rate_percent"]}%
Recent change: {health_data["recent_change"]}

Decision:
No immediate action required.
"""

    return f"""
Service: {health_data["service"]}
Status: DEGRADED

Availability: {health_data["availability"]}
P95 latency: {health_data["latency_p95_ms"]} ms
Error rate: {health_data["error_rate_percent"]}%
Recent change: {health_data["recent_change"]}

Likely cause:
Recent deployment or elevated downstream errors.

Recommended action:
Investigate the recent change, check dependency health, and confirm rollback readiness.
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