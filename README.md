# SecureOps AI -- UiPath AgentHack 2026

**Track 1: UiPath Maestro Case**

AI-powered security alert triage that turns overwhelming alert volumes into decisive, routed actions -- autonomously.

## The Problem

Security teams receive hundreds of alerts daily. Manual triage is slow, inconsistent, and expensive. Mean time to respond (MTTR) averages 280 days for undetected breaches.

## The Solution

SecureOps AI uses Claude AI + UiPath Maestro to:
1. Receive security alerts from any source (SIEM, email, webhook)
2. Classify severity (Critical/High/Medium/Low) using AI analysis
3. Extract threat indicators, affected systems, and recommended actions
4. Route each case through Maestro with the right escalation path
5. Generate audit-ready incident reports automatically

## Architecture

```
Alert Source -> Webhook/Polling Agent
                        |
               Claude AI Analyzer
               (severity + indicators + remediation)
                        |
              UiPath Maestro Case Router
              /        |         \       \
        Critical    High      Medium    Low
           |          |          |        |
     Page on-call  Create     Open     Auto-
     + Exec alert  P2 ticket  P3 log   remediate
     + War room    + Notify   + Notify  + close
```

## Tech Stack

- **UiPath Maestro**: Case orchestration and routing
- **Claude API (claude-sonnet-4-6)**: AI analysis and classification
- **Python**: Agent runtime
- **UiPath Studio**: Workflow definitions

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
export UIPATH_CLIENT_ID=your_client_id
export UIPATH_CLIENT_SECRET=your_client_secret
export UIPATH_ORG_ID=your_org_id
python agent/main.py
```

## Demo

Run the demo with sample alerts:
```bash
python agent/main.py --demo
```

## Competition Details

- UiPath AgentHack 2026 -- Track 1: UiPath Maestro Case
- Team: AppZ AI Studio (zac@getactcomply.com)
- Built with Claude Code
