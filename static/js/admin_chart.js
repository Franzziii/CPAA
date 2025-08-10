// Initialize all charts on page load
document.addEventListener('DOMContentLoaded', function() {
    renderTypeChart();
    renderStatusChart();
    renderTrendChart();
});

// Crime Type Distribution Chart
function renderTypeChart() {
    const ctx = document.getElementById('typeChart').getContext('2d');
    const typeData = JSON.parse('{{ crime_types|tojson|safe }}');
    
    const labels = typeData.map(item => item.incident_type);
    const data = typeData.map(item => item.count);
    const backgroundColors = [
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)'
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Reports',
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Crime Type Distribution',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Crime Status Distribution Chart
function renderStatusChart() {
    const ctx = document.getElementById('statusChart').getContext('2d');
    const statusData = JSON.parse('{{ status_dist|tojson|safe }}');
    
    const labels = statusData.map(item => item.status);
    const data = statusData.map(item => item.count);
    const backgroundColors = [
        'rgba(255, 206, 86, 0.7)',  // Pending - yellow
        'rgba(54, 162, 235, 0.7)',  // Received - blue
        'rgba(255, 159, 64, 0.7)',  // Under Investigation - orange
        'rgba(75, 192, 192, 0.7)'   // Resolved - teal
    ];

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Crime Status Distribution',
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

// Monthly Crime Trend Chart
function renderTrendChart() {
    const ctx = document.getElementById('trendChart').getContext('2d');
    const trendData = JSON.parse('{{ monthly_trend|tojson|safe }}');
    
    const labels = trendData.map(item => item.month);
    const data = trendData.map(item => item.count);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Reports',
                data: data,
                borderColor: 'rgba(54, 162, 235, 0.8)',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Monthly Crime Trend',
                    font: {
                        size: 16
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

// Download chart as image
function downloadChart(chartId) {
    const canvas = document.getElementById(chartId);
    const link = document.createElement('a');
    link.download = `${chartId}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}