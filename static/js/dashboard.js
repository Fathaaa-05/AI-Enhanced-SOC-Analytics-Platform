function createChartIfExists(elementId, config) {
    const element = document.getElementById(elementId);

    if (element) {
        new Chart(element, config);
    }
}

if (typeof attackLabels !== "undefined") {
    createChartIfExists("attackChart", {
        type: "bar",
        data: {
            labels: attackLabels,
            datasets: [{
                label: "Detected Attacks",
                data: attackLabels.map(() => 1)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: "#e2e8f0" }
                }
            },
            scales: {
                x: { ticks: { color: "#94a3b8" } },
                y: { ticks: { color: "#94a3b8" } }
            }
        }
    });
}

if (typeof severityData !== "undefined") {
    createChartIfExists("severityChart", {
        type: "pie",
        data: {
            labels: ["High", "Medium", "Low"],
            datasets: [{
                data: severityData
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: "#e2e8f0" }
                }
            }
        }
    });
}

if (typeof analyticsAttackLabels !== "undefined") {
    createChartIfExists("analyticsAttackChart", {
        type: "bar",
        data: {
            labels: analyticsAttackLabels,
            datasets: [{
                label: "Attack Types",
                data: analyticsAttackLabels.map(() => 1)
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: "#e2e8f0" }
                }
            },
            scales: {
                x: { ticks: { color: "#94a3b8" } },
                y: { ticks: { color: "#94a3b8" } }
            }
        }
    });
}

if (typeof analyticsSeverityData !== "undefined") {
    createChartIfExists("analyticsSeverityChart", {
        type: "doughnut",
        data: {
            labels: ["High", "Medium", "Low"],
            datasets: [{
                data: analyticsSeverityData
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: { color: "#e2e8f0" }
                }
            }
        }
    });
}

let previousAlertCount = null;

async function refreshDashboardSummary() {
    try {
        const response = await fetch("/api/dashboard-summary");

        if (!response.ok) {
            return;
        }

        const data = await response.json();

        const totalLogs = document.getElementById("totalLogs");
        const totalAlerts = document.getElementById("totalAlerts");
        const totalIncidents = document.getElementById("totalIncidents");
        const totalAIAnomalies = document.getElementById("totalAIAnomalies");
        const criticalUsers = document.getElementById("criticalUsers");

        if (totalLogs) {
            totalLogs.textContent = data.total_logs;
        }

        if (totalAlerts) {
            totalAlerts.textContent = data.total_alerts;
        }

        if (totalIncidents) {
            totalIncidents.textContent = data.total_incidents;
        }

        if (totalAIAnomalies) {
            totalAIAnomalies.textContent = data.ai_anomalies;
        }

        if (criticalUsers) {
            criticalUsers.textContent = data.critical_users;
        }

        if (
            previousAlertCount !== null &&
            data.total_alerts > previousAlertCount
        ) {
            showLiveToast(
                `${data.total_alerts - previousAlertCount} new alert(s) detected`
            );
        }

        previousAlertCount = data.total_alerts;

    } catch (error) {
        console.error("Dashboard refresh failed:", error);
    }
}


function showLiveToast(message) {
    const toast = document.getElementById("liveToast");

    if (!toast) {
        return;
    }

    toast.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 4000);
}


refreshDashboardSummary();

setInterval(refreshDashboardSummary, 5000);