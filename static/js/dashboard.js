new Chart(document.getElementById("attackChart"), {
    type: "bar",
    data: {
        labels: attackLabels,
        datasets: [{
            label: "Detected Attacks",
            data: attackLabels.map(() => 1)
        }]
    }
});

new Chart(document.getElementById("severityChart"), {
    type: "pie",
    data: {
        labels: ["High", "Medium", "Low"],
        datasets: [{
            data: severityData
        }]
    }
});