import sys
import os
import json
from dotenv import load_dotenv
from sre_agent.tools.monitoring_tools import get_service_health
from sre_agent.analysis.incident_analyzer import build_incident_analysis
from sre_agent.ai.gemini_explainer import generate_ai_explanation
from sre_agent.reporting.report_formatter import format_report


load_dotenv()




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sre_agent/agent.py <service_name>")
        print("Example: python sre_agent/agent.py checkout")
        sys.exit(1)

    service_name = sys.argv[1]

    health = get_service_health(service_name)
    analysis = build_incident_analysis(health)
    ai_explanation = generate_ai_explanation(health, analysis)

    print(format_report(analysis, ai_explanation, execution_mode="Direct Python tool agent"))

    print("Structured JSON output:")
    print(json.dumps(analysis, indent=2))