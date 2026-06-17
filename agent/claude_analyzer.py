import anthropic
import json
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client

SYSTEM_PROMPT = """You are a senior security analyst AI integrated into a security operations center (SOC).
Analyze security alerts and provide structured triage decisions.

Always respond with valid JSON matching this exact schema:
{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "confidence": 0.0-1.0,
  "threat_type": "string",
  "affected_systems": ["string"],
  "indicators": ["string"],
  "immediate_actions": ["string"],
  "containment_steps": ["string"],
  "false_positive_risk": "HIGH|MEDIUM|LOW",
  "false_positive_reason": "string or null",
  "escalate_to_human": true|false,
  "summary": "one sentence summary for incident ticket"
}

Severity definitions:
- CRITICAL: Active breach, data exfiltration in progress, ransomware, executive system compromised
- HIGH: Successful malware execution, confirmed credential theft, lateral movement detected
- MEDIUM: Suspicious activity likely malicious but no confirmed breach, phishing blocked
- LOW: Reconnaissance, failed attacks, policy violations with no data exposure"""

MOCK_DATA = None

def _load_mock():
    global MOCK_DATA
    if MOCK_DATA is None:
        mock_path = os.path.join(os.path.dirname(__file__), "..", "demo", "mock_analyses.json")
        with open(mock_path) as f:
            MOCK_DATA = json.load(f)
    return MOCK_DATA


def analyze_alert(alert: dict, mock: bool = False) -> dict:
    if mock or not os.getenv("ANTHROPIC_API_KEY"):
        data = _load_mock()
        alert_id = alert.get("id", "")
        if alert_id in data:
            return data[alert_id]
        return {"severity": "MEDIUM", "confidence": 0.5, "threat_type": "Unknown", "affected_systems": [], "indicators": [], "immediate_actions": [], "containment_steps": [], "false_positive_risk": "MEDIUM", "false_positive_reason": None, "escalate_to_human": True, "summary": "Alert requires manual review"}
    prompt = f"""Analyze this security alert and provide triage:

Alert ID: {alert.get('id', 'unknown')}
Source: {alert.get('source', 'unknown')}
Host/System: {alert.get('host', 'unknown')}
Alert Type: {alert.get('type', 'unknown')}
Raw Alert Details:
{alert.get('raw', '')}

Respond with JSON only."""

    response = _get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)
