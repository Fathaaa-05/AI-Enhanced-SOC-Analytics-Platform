new Chart(document.getElementById("attackChart"), {
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
                labels: {
                    color: "#e2e8f0"
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: "#94a3b8"
                }
            },
            y: {
                ticks: {
                    color: "#94a3b8"
                }
            }
        }
    }
});

new Chart(document.getElementById("severityChart"), {
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
                labels: {
                    color: "#e2e8f0"
                }
            }
        }
    }
});