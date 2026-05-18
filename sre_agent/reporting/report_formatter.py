def format_report(analysis: dict, ai_explanation: str, execution_mode: str):
    evidence = analysis["evidence"]

    return f"""
================ SRE INCIDENT TRIAGE REPORT ================

Execution mode: {execution_mode}

Service: {analysis["service"]}
Status: {analysis["status"].upper()}
Severity: {analysis["severity"]}

Evidence:
- Availability: {evidence["availability"]}
- P95 latency: {evidence["latency_p95_ms"]} ms
- Error rate: {evidence["error_rate_percent"]}%
- Recent change: {evidence["recent_change"]}

Likely cause:
{analysis["likely_cause"]}

Recommended action:
{analysis["recommended_action"]}

Leadership summary:
{analysis["leadership_summary"]}

AI-generated incident explanation:
{ai_explanation}

============================================================
"""