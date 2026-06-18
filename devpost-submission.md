# DevPost Submission -- SecureOps AI

Track: UiPath Maestro Case
Team: AppZ AI Studio
GitHub: https://github.com/AppZ3/secureops-ai

---

## Inspiration

Security teams in 2026 are drowning. The average enterprise SOC analyst handles 11,000 security alerts per day. Manual triage is slow, inconsistent, and exhausting. Critical alerts get buried under noise. Breaches go undetected for an average of 204 days -- not because the alert wasn't generated, but because no one had time to look at it.

The real problem isn't a shortage of alerts. It's a shortage of consistent, fast, intelligent triage.

We built SecureOps AI to solve the triage layer so human analysts can focus on the work that actually requires human judgment: investigating confirmed incidents, making containment decisions under pressure, and handling the cases that fall outside normal patterns.

## What It Does

SecureOps AI is an AI-powered security alert triage system that integrates Claude AI with UiPath Maestro to turn raw security alerts into routed, prioritised, action-ready cases -- automatically.

When a security alert arrives (from a SIEM like Splunk, an EDR like CrowdStrike, a cloud platform like AWS GuardDuty, or any other source via webhook):

1. **Claude AI analyzes the alert** in seconds. It classifies severity (CRITICAL, HIGH, MEDIUM, LOW), extracts threat indicators (IOCs), identifies affected systems, lists immediate containment actions, flags whether human escalation is needed, and assigns a confidence score.

2. **UiPath Maestro creates a case** with all this context, routes it to the right response path based on severity, and sets the appropriate SLA timer.

3. **The right response happens automatically**: CRITICAL alerts page the on-call engineer and notify executives immediately. HIGH alerts generate P2 tickets and block IOCs. MEDIUM alerts are assigned to a human analyst with a 4-hour SLA. LOW alerts are auto-remediated and closed with full audit logging.

Human analysts are looped in exactly when they should be: for critical incidents requiring judgment, and whenever Claude's confidence drops below 70% (flagged for human review).

## How We Built It

The agent pipeline is in Python. Claude claude-sonnet-4-6 handles the AI analysis layer -- given the raw alert text, it returns a structured JSON with severity classification, confidence, threat type, IOCs, affected systems, and recommended actions. The system prompt encodes expert SOC analyst knowledge for consistent, security-aware reasoning.

The Maestro integration uses UiPath Automation Cloud's REST API. Each analyzed alert creates a Maestro case with the full AI analysis payload, type-appropriate routing, and SLA configuration. The case definition in `maestro/case_definition.json` defines the stage flow: ingestion, AI analysis, severity routing, response (four parallel paths based on severity), optional human review, and case closure.

The project runs fully in demo mode without API credentials (pre-computed analyses for 5 realistic alert scenarios), and switches to live mode when ANTHROPIC_API_KEY and UiPath credentials are set.

## Challenges

Getting Claude to produce consistent, parseable JSON under adversarial alert content (malformed logs, foreign character sets, base64-encoded payloads like the PowerShell macro in our demo) required careful prompt engineering. The system prompt defines severity thresholds, response schema, and edge case handling explicitly.

The Maestro case routing architecture required thinking carefully about the tradeoffs: fully automated response is fast but loses auditability; pure human-in-the-loop doesn't scale. The solution was tiered automation with confidence-gated human review -- high-confidence classifications run automatically, low-confidence ones pause for analyst review.

## Accomplishments

- Full triage pipeline from raw alert to routed Maestro case in under 3 seconds
- 5 realistic demo scenarios covering all severity levels (SIEM brute force, EDR malware execution, Cloud credential access, internal reconnaissance, phishing)
- Confidence-gated human escalation (automatic review when Claude confidence < 70%)
- Clean separation between demo mode (no credentials) and live mode (full Maestro API integration)
- Maestro case definition ready for import to UiPath Automation Cloud

## What We Learned

The most important insight: AI handles the volume, humans handle the judgment. The system performs best when the boundary between these is explicit -- not "AI does everything" or "AI just suggests", but a defined contract where AI makes decisions within well-specified confidence bounds and escalates cleanly at the boundary.

UiPath Maestro's case-centric model maps naturally to security incident management. Cases persist across stage transitions, carry the full investigation context, and support human handoffs without losing state -- exactly what SOC workflows need.

## What's Next

- Webhook endpoint for real-time alert ingestion from any SIEM
- UiPath Studio workflow for automated IOC blocking (firewall rule updates)
- Historical case data feedback loop to improve Claude's severity calibration
- Integration with ticketing systems (ServiceNow, Jira) for P2/P3 case handoff
- Multi-tenant support for MSSPs managing multiple client environments

---

## Built With

- Python
- Anthropic Claude claude-sonnet-4-6
- UiPath Maestro
- UiPath Automation Cloud
