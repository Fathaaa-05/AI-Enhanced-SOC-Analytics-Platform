def calculate_incident_risk(incident, related_logs):
    score = 20
    reasons = []

    severity = str(incident.get("severity", "")).lower()
    attack = str(incident.get("attack", "")).lower()

    # Severity contribution
    severity_scores = {
        "low": 10,
        "medium": 25,
        "high": 45,
        "critical": 60,
    }

    score += severity_scores.get(severity, 15)

    if severity in {"high", "critical"}:
        reasons.append(f"{severity.title()} severity incident")

    # Attack contribution
    if "brute force" in attack:
        score += 15
        reasons.append("Repeated authentication attack")

    elif "privileged" in attack or "privilege" in attack:
        score += 20
        reasons.append("Privileged account activity")

    elif "port scan" in attack:
        score += 12
        reasons.append("Network reconnaissance activity")

    elif "account creation" in attack:
        score += 18
        reasons.append("Suspicious account-management activity")

    # Related evidence contribution
    high_events = sum(
        1
        for log in related_logs
        if str(log.get("severity", "")).lower() in {"high", "critical"}
    )

    failed_logins = sum(
        1
        for log in related_logs
        if "failed login" in str(log.get("status", "")).lower()
    )

    score += min(high_events * 3, 15)
    score += min(failed_logins * 2, 10)

    if high_events:
        reasons.append(f"{high_events} related high-risk event(s)")

    if failed_logins:
        reasons.append(f"{failed_logins} related failed login(s)")

    score = min(score, 100)

    if score >= 85:
        threat_level = "Critical"
    elif score >= 65:
        threat_level = "High"
    elif score >= 40:
        threat_level = "Medium"
    else:
        threat_level = "Low"

    recommendations = generate_recommendations(attack, threat_level)

    return {
        "score": score,
        "confidence": min(75 + len(related_logs), 98),
        "threat_level": threat_level,
        "reasons": reasons,
        "recommendations": recommendations,
    }


def generate_recommendations(attack, threat_level):
    recommendations = [
        "Review the related security logs.",
        "Validate activity with the affected user.",
    ]

    if "brute force" in attack:
        recommendations.extend([
            "Temporarily block the suspicious source IP.",
            "Reset the affected account password.",
            "Enable multi-factor authentication.",
        ])

    elif "port scan" in attack:
        recommendations.extend([
            "Review firewall activity from the source IP.",
            "Block unauthorized scanning traffic.",
            "Check exposed services and open ports.",
        ])

    elif "privileged" in attack or "privilege" in attack:
        recommendations.extend([
            "Verify whether the privileged logon was authorized.",
            "Review administrative actions after the logon.",
            "Restrict unnecessary privileged access.",
        ])

    elif "account creation" in attack:
        recommendations.extend([
            "Confirm that the new account was authorized.",
            "Review the account's permissions and group membership.",
            "Disable the account if it is unrecognized.",
        ])

    if threat_level == "Critical":
        recommendations.insert(
            0,
            "Escalate immediately to the incident-response team.",
        )

    return recommendations