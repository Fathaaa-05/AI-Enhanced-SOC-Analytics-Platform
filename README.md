# 🛡️ AI-Enhanced SOC Analytics Platform

A Flask-based Security Operations Center (SOC) platform for log analysis, threat detection, AI anomaly detection, incident management, analytics, and automated PDF reporting.

## 🚀 Features

- User authentication and session management
- Windows, Linux, and firewall log collection
- Log parsing and normalization
- Rule-based threat detection
  - Brute force attacks
  - Port scanning
  - Suspicious activity
- MITRE ATT&CK mapping
- AI anomaly detection using Isolation Forest
- User risk scoring engine
- Alerts dashboard
- Incident management
- Security analytics dashboard
- PDF incident report generation
- Professional dark SOC-style UI
- MySQL database integration

## 🧠 Technologies Used

- Python
- Flask
- MySQL
- Scikit-learn
- Pandas
- Chart.js
- ReportLab
- HTML
- CSS
- JavaScript
- Git

## 📂 Project Structure

```text
soc-ai-platform/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── ai/
│   ├── auth/
│   ├── collector/
│   ├── dashboard/
│   ├── database/
│   ├── detection/
│   ├── generator/
│   ├── parser/
│   └── reports/
│
├── templates/
│   ├── layout.html
│   ├── login.html
│   ├── dashboard.html
│   ├── alerts.html
│   ├── incidents.html
│   ├── ai.html
│   ├── analytics.html
│   └── reports.html
│
├── static/
│   ├── css/
│   └── js/
│
├── data/
└── reports_output/