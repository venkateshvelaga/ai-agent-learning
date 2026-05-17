import os
import sys
import requests


def get_service_health(service_name: str):
    """
    Tool: Fetch service health from the mock monitoring API.
    """
    base_url = os.getenv("MONITORING_API_BASE_URL", "http://127.0.0.1:8000")
    url = f"{base_url}/health/{service_name}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to mock monitoring API.")
        print("Make sure it is running with:")
        print("uvicorn mock_monitoring_api.main:app --reload")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("ERROR: Request to mock monitoring API timed out.")
        sys.exit(1)

    except requests.exceptions.HTTPError as error:
        print(f"ERROR: Mock monitoring API returned an HTTP error: {error}")
        sys.exit(1)

    except requests.exceptions.JSONDecodeError:
        print("ERROR: Mock monitoring API returned invalid JSON.")
        sys.exit(1)

    except requests.exceptions.RequestException as error:
        print(f"ERROR: Request failed: {error}")
        sys.exit(1)