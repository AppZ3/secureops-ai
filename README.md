# SecureOps AI -- AI-Powered Security Alert Triage

**UiPath AgentHack 2026 | Track 1: UiPath Maestro Case**

SecureOps AI turns security alert avalanches into decisive, routed actions using Claude AI for instant triage and UiPath Maestro for case orchestration. Security teams receive hundreds of alerts daily. Mean time to detect (MTTD) averages 204 days for breaches -- SecureOps cuts initial triage from hours to seconds.

---

## How It Works

```
Alert Sources                     SecureOps AI                     UiPath Maestro
(SIEM / EDR / Cloud / Email)          |                                  |
         |                    Claude AI Analyzer                         |
         |                    - Severity: CRITICAL/HIGH/MEDIUM/LOW       |
         +---> Webhook -----> - Confidence score (0-100%)      -------> Case Router
                              - Threat type + IOC extraction              |
                              - Affected systems                   +------+------+------+
                              - Immediate actions                  |      |      |      |
                              - Human escalation flag             P1     P2     P3     P4
                                                                Critical High  Med   Low
                                                                  |      |      |      |
                                                              Page    Create  Assign  Auto-
                                                             OnCall  P2 Ticket Human  Close
                                                             + Exec   + Block  Review
                                                             Alert    IOCs
```

**Case stages (Maestro):**

| Stage | Type | SLA | Actions |
|-------|------|-----|---------|
| Alert Ingestion | Automated | -- | Receive + normalize |
| Claude AI Analysis | Automated | -- | Classify + extract threat intel |
| Severity Router | Decision | -- | Branch to appropriate response path |
| CRITICAL Response | Automated | 15 min | Page on-call, notify exec, isolate host, open war room |
| HIGH Response | Automated | 60 min | Create P2 ticket, notify team, block IOCs |
| MEDIUM Response | Human | 4 hrs | Assign analyst, human review required |
| LOW Response | Automated | 24 hrs | Auto-remediate, log, close |
| Human Review | Human (optional) | -- | Triggered when Claude confidence < 70% |
| Case Closed | Terminal | -- | Report generated, post-mortem if P1/P2 |

---

## Demo

Run the demo with sample alerts (no API keys needed -- uses pre-computed mock analyses):

```bash
python3 agent/main.py --demo
```

Output:
```
SecureOps AI -- AI-Powered Security Alert Triage
UiPath AgentHack 2026 | Track 1: Maestro Case
Processing 5 sample security alerts...

Analyzing ALERT-001 from Splunk SIEM...
  HIGH confidence=92% -- SSH brute force from threat-intel-flagged IP targeting prod-db-01
  Maestro: Would create SecurityIncident case with priority P2

Analyzing ALERT-002 from CrowdStrike EDR...
  CRITICAL confidence=97% -- Macro-triggered PowerShell downloading payload -- active malware
  Maestro: Would create SecurityIncident case with priority P1

...

Triage Summary: 1 CRITICAL, 2 HIGH, 1 MEDIUM, 1 LOW
All cases routed to Maestro with appropriate SLAs and human escalation flags
```

---

## Technical Stack

| Component | Technology |
|-----------|------------|
| AI Analysis | Claude claude-sonnet-4-6 (Anthropic) |
| Case Orchestration | UiPath Maestro (Automation Cloud) |
| Agent Runtime | Python 3.x |
| Alert Sources | Any (webhook, Splunk SIEM, CrowdStrike, AWS GuardDuty, Firewall, Email Gateway) |
| Output | UiPath case with severity, IOCs, actions, SLA, and human escalation flag |

---

## Why This Matters

Security Operations Center (SOC) teams in 2026:
- Receive an average of **11,000 security alerts per day** per analyst
- Spend **76% of their time** on alert triage rather than response
- Face a **340,000 unfilled cybersecurity job** shortage globally
- Average **204 days** to detect a breach (often because alerts were missed)

SecureOps AI handles the triage layer instantly -- high confidence, consistent, never fatigued. Humans review only the cases that need them (low-confidence classifications, critical incidents requiring judgment).

---

## Setup

**Requirements:**
- `ANTHROPIC_API_KEY` -- for live Claude analysis (demo mode works without it)
- `UIPATH_CLIENT_ID` + `UIPATH_CLIENT_SECRET` + `UIPATH_ORG_ID` -- for live Maestro routing (demo mode works without it)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Demo mode (no credentials needed)
python3 agent/main.py --demo

# Live mode (requires API keys)
export ANTHROPIC_API_KEY=your_key
export UIPATH_CLIENT_ID=your_client_id
export UIPATH_CLIENT_SECRET=your_client_secret
export UIPATH_ORG_ID=your_org_id
python3 agent/main.py --demo  # or --alert '{"id": "...", "raw": "..."}'
```

---

## Project Structure

```
secureops-ai/
  agent/
    main.py             -- Entry point: orchestrates triage pipeline
    claude_analyzer.py  -- Claude AI integration for alert analysis
    maestro_client.py   -- UiPath Maestro REST API client
  maestro/
    case_definition.json -- Maestro case type definition (import to Automation Cloud)
  demo/
    sample_alerts.json  -- 5 realistic security alerts across all severity levels
    mock_analyses.json  -- Pre-computed analyses for demo mode (no API key needed)
  requirements.txt
```

---

## Competition Details

- **Competition**: UiPath AgentHack 2026
- **Track**: Track 1 -- UiPath Maestro Case
- **Team**: AppZ AI Studio (zac@getactcomply.com)
- **DevPost**: https://uipath-agenthack.devpost.com/
- **Built with**: Claude Code
