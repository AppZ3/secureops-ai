"""
UiPath Maestro API client.
In Labs environment: uses real Maestro REST API.
Without Labs: prints what Maestro would do (demo mode).
"""
import os
import json
import httpx
from datetime import datetime

MAESTRO_BASE = "https://cloud.uipath.com/{org_id}/maestro_/api"

SEVERITY_ROUTES = {
    "CRITICAL": {
        "case_type": "SecurityIncident",
        "priority": "P1",
        "actions": ["page_oncall", "notify_exec", "create_war_room", "isolate_host"],
        "sla_minutes": 15,
    },
    "HIGH": {
        "case_type": "SecurityIncident",
        "priority": "P2",
        "actions": ["create_ticket", "notify_security_team", "block_ioc"],
        "sla_minutes": 60,
    },
    "MEDIUM": {
        "case_type": "SecurityAlert",
        "priority": "P3",
        "actions": ["create_ticket", "notify_analyst", "log_ioc"],
        "sla_minutes": 240,
    },
    "LOW": {
        "case_type": "SecurityLog",
        "priority": "P4",
        "actions": ["auto_remediate", "log_and_close"],
        "sla_minutes": 1440,
    },
}


def _get_token() -> str | None:
    client_id = os.getenv("UIPATH_CLIENT_ID")
    client_secret = os.getenv("UIPATH_CLIENT_SECRET")
    if not client_id or not client_secret:
        return None
    resp = httpx.post(
        "https://cloud.uipath.com/identity_/connect/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "OR.Cases OR.Cases.Write",
        },
    )
    if resp.status_code == 200:
        return resp.json()["access_token"]
    return None


def route_case(alert: dict, analysis: dict, demo: bool = False) -> dict:
    severity = analysis.get("severity", "MEDIUM")
    route = SEVERITY_ROUTES.get(severity, SEVERITY_ROUTES["MEDIUM"])

    case_payload = {
        "title": f"[{route['priority']}] {analysis.get('summary', alert.get('id', 'Security Alert'))}",
        "caseType": route["case_type"],
        "priority": route["priority"],
        "alertId": alert.get("id"),
        "source": alert.get("source"),
        "affectedSystems": analysis.get("affected_systems", []),
        "indicators": analysis.get("indicators", []),
        "immediateActions": analysis.get("immediate_actions", []),
        "containmentSteps": analysis.get("containment_steps", []),
        "severity": severity,
        "confidence": analysis.get("confidence", 0.8),
        "threatType": analysis.get("threat_type", "Unknown"),
        "escalateToHuman": analysis.get("escalate_to_human", True),
        "slaDueMinutes": route["sla_minutes"],
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "rawAlert": alert.get("raw", ""),
    }

    if demo:
        return {
            "status": "DEMO",
            "maestro_action": f"Would create {route['case_type']} case with priority {route['priority']}",
            "automated_actions": route["actions"],
            "case_payload": case_payload,
        }

    token = _get_token()
    if not token:
        return {
            "status": "NO_LABS_CREDS",
            "note": "Set UIPATH_CLIENT_ID and UIPATH_CLIENT_SECRET for live Maestro routing",
            "case_payload": case_payload,
        }

    org_id = os.getenv("UIPATH_ORG_ID", "appzaistudio")
    base = MAESTRO_BASE.format(org_id=org_id)
    resp = httpx.post(
        f"{base}/cases",
        json=case_payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=30,
    )
    if resp.status_code in (200, 201):
        return {"status": "CREATED", "case": resp.json()}
    return {"status": "ERROR", "code": resp.status_code, "body": resp.text}
