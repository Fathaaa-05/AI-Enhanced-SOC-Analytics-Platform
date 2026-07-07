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