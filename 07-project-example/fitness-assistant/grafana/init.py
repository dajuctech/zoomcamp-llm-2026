import os
import time
from pathlib import Path

import requests


GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
GRAFANA_USER = os.getenv("GRAFANA_USER", "admin")
GRAFANA_PASSWORD = os.getenv("GRAFANA_PASSWORD", "admin")

DATASOURCE_UID = "fitness-postgres"
DATASOURCE_NAME = "fitness-postgres"


def wait_for_grafana():
    for _ in range(30):
        try:
            response = requests.get(
                f"{GRAFANA_URL}/api/health",
                auth=(GRAFANA_USER, GRAFANA_PASSWORD),
                timeout=2,
            )

            if response.status_code == 200:
                return

        except requests.RequestException:
            pass

        time.sleep(2)

    raise RuntimeError("Grafana is not ready")


def create_datasource():
    response = requests.get(
        f"{GRAFANA_URL}/api/datasources/uid/{DATASOURCE_UID}",
        auth=(GRAFANA_USER, GRAFANA_PASSWORD),
        timeout=5,
    )

    if response.status_code == 200:
        print("Data source already exists")
        return

    payload = {
        "name": DATASOURCE_NAME,
        "uid": DATASOURCE_UID,
        "type": "grafana-postgresql-datasource",
        "access": "proxy",
        "url": "postgres:5432",
        "user": "user",
        "database": "fitness_assistant",
        "basicAuth": False,
        "isDefault": True,
        "jsonData": {
            "sslmode": "disable",
            "postgresVersion": 1700,
        },
        "secureJsonData": {
            "password": "password",
        },
    }

    response = requests.post(
        f"{GRAFANA_URL}/api/datasources",
        json=payload,
        auth=(GRAFANA_USER, GRAFANA_PASSWORD),
        timeout=5,
    )
    response.raise_for_status()

    print("Data source created")


def load_dashboard():
    dashboard_path = Path(__file__).with_name("dashboard.json")
    dashboard = dashboard_path.read_text()

    payload = {
        "dashboard": requests.models.complexjson.loads(dashboard),
        "overwrite": True,
        "folderId": 0,
        "message": "Load fitness assistant dashboard",
    }

    response = requests.post(
        f"{GRAFANA_URL}/api/dashboards/db",
        json=payload,
        auth=(GRAFANA_USER, GRAFANA_PASSWORD),
        timeout=5,
    )
    response.raise_for_status()

    result = response.json()
    print("Dashboard loaded")
    print(f"{GRAFANA_URL}{result['url']}")


if __name__ == "__main__":
    wait_for_grafana()
    create_datasource()
    load_dashboard()
