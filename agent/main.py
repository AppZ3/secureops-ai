#!/usr/bin/env python3
"""
SecureOps AI -- AI-Powered Security Alert Triage
UiPath AgentHack 2026, Track 1: Maestro Case

Receives security alerts, uses Claude AI to analyze severity and extract
threat intelligence, then routes each case through UiPath Maestro.
"""
import sys
import json
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from claude_analyzer import analyze_alert
from maestro_client import route_case

console = Console()

SEVERITY_COLORS = {
    "CRITICAL": "bold red",
    "HIGH": "red",
    "MEDIUM": "yellow",
    "LOW": "green",
}


def process_alert(alert: dict, demo: bool = False) -> dict:
    console.print(f"\n[dim]Analyzing alert {alert.get('id', '?')} from {alert.get('source', '?')}...[/dim]")

    analysis = analyze_alert(alert)
    severity = analysis.get("severity", "MEDIUM")
    color = SEVERITY_COLORS.get(severity, "white")

    console.print(f"  [{color}]{severity}[/{color}] confidence={analysis.get('confidence', 0):.0%} -- {analysis.get('summary', '')}")

    result = route_case(alert, analysis, demo=demo)
    action = result.get("maestro_action") or result.get("status", "")
    console.print(f"  [dim]Maestro: {action}[/dim]")

    return {"alert": alert, "analysis": analysis, "routing": result}


def run_demo():
    demo_path = Path(__file__).parent.parent / "demo" / "sample_alerts.json"
    alerts = json.loads(demo_path.read_text())

    console.print(Panel.fit(
        "[bold cyan]SecureOps AI[/bold cyan] -- AI-Powered Security Alert Triage\n"
        "UiPath AgentHack 2026 | Track 1: Maestro Case\n"
        f"Processing [bold]{len(alerts)}[/bold] sample security alerts...",
        border_style="cyan"
    ))

    results = []
    for alert in alerts:
        results.append(process_alert(alert, demo=True))

    table = Table(title="\nTriage Summary", box=box.ROUNDED, border_style="cyan")
    table.add_column("Alert ID", style="dim")
    table.add_column("Source")
    table.add_column("Threat Type")
    table.add_column("Severity")
    table.add_column("Confidence")
    table.add_column("Action")
    table.add_column("Escalate")

    for r in results:
        a = r["analysis"]
        severity = a.get("severity", "?")
        color = SEVERITY_COLORS.get(severity, "white")
        routing = r["routing"]
        actions = routing.get("automated_actions", [])
        table.add_row(
            r["alert"].get("id", "?"),
            r["alert"].get("source", "?"),
            a.get("threat_type", "?"),
            f"[{color}]{severity}[/{color}]",
            f"{a.get('confidence', 0):.0%}",
            ", ".join(actions[:2]),
            "YES" if a.get("escalate_to_human") else "no",
        )

    console.print(table)

    output_path = Path(__file__).parent.parent / "demo" / "demo_output.json"
    output_path.write_text(json.dumps(results, indent=2))
    console.print(f"\n[dim]Full output saved to {output_path}[/dim]")


def run_live(alert_json: str):
    alert = json.loads(alert_json)
    result = process_alert(alert, demo=False)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SecureOps AI -- Alert Triage Agent")
    parser.add_argument("--demo", action="store_true", help="Run demo with sample alerts")
    parser.add_argument("--alert", type=str, help="JSON string of a single alert to process")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.alert:
        run_live(args.alert)
    else:
        console.print("[yellow]Use --demo to run with sample alerts, or --alert '{...}' for a single alert[/yellow]")
        sys.exit(1)
