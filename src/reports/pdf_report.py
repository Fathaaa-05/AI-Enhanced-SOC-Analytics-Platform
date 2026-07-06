from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.database.fetch_logs import fetch_logs
from src.database.fetch_alerts import fetch_alerts
from src.database.incidents import fetch_incidents
from src.dashboard.ai_service import get_ai_anomalies


BASE_DIR = Path(__file__).resolve().parents[2]
REPORT_DIR = BASE_DIR / "reports_output"
REPORT_DIR.mkdir(exist_ok=True)


def generate_incident_report():
    logs = fetch_logs()
    alerts = fetch_alerts()
    incidents = fetch_incidents()
    ai_anomalies = get_ai_anomalies()

    filename = REPORT_DIR / f"soc_incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    pdf = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4

    y = height - 50

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "AI-Enhanced SOC Analytics Platform")
    y -= 30

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Security Incident Report")
    y -= 40

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Executive Summary")
    y -= 25

    pdf.setFont("Helvetica", 11)
    summary = [
        f"Total Logs Processed: {len(logs)}",
        f"Total Alerts Detected: {len(alerts)}",
        f"Total Incidents Created: {len(incidents)}",
        f"AI Anomalies Detected: {len(ai_anomalies)}",
    ]

    for item in summary:
        pdf.drawString(70, y, item)
        y -= 20

    y -= 20
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Recent Alerts")
    y -= 25

    pdf.setFont("Helvetica", 10)

    for alert in alerts[:10]:
        text = f"- {alert['attack']} | IP: {alert['source_ip']} | Severity: {alert['severity']} | MITRE: {alert['mitre_technique']}"
        pdf.drawString(70, y, text[:110])
        y -= 18

        if y < 80:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)

    y -= 20
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Recommended Actions")
    y -= 25

    pdf.setFont("Helvetica", 11)
    recommendations = [
        "Enable multi-factor authentication for privileged accounts.",
        "Block suspicious source IP addresses.",
        "Review authentication logs for affected users.",
        "Investigate high-risk users and open incidents.",
        "Update firewall and access control policies.",
    ]

    for rec in recommendations:
        pdf.drawString(70, y, f"- {rec}")
        y -= 20

    pdf.save()

    print(f"✅ PDF report generated: {filename}")


if __name__ == "__main__":
    generate_incident_report()