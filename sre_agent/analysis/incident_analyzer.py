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


def build_incident_analysis(health_data: dict):
    severity = classify_severity(health_data)
    likely_cause = find_likely_cause(health_data)
    action = recommend_action(severity)

    return {
        "service": health_data["service"],
        "status": health_data["status"],
        "severity": severity,
        "evidence": {
            "availability": health_data["availability"],
            "latency_p95_ms": health_data["latency_p95_ms"],
            "error_rate_percent": health_data["error_rate_percent"],
            "recent_change": health_data["recent_change"],
        },
        "likely_cause": likely_cause,
        "recommended_action": action,
        "leadership_summary": (
            f'{health_data["service"]} is currently {health_data["status"]} '
            f'with severity {severity}. Main signals: availability '
            f'{health_data["availability"]}, p95 latency '
            f'{health_data["latency_p95_ms"]} ms, error rate '
            f'{health_data["error_rate_percent"]}%.'
        ),
    }