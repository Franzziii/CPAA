function renderCharts() {
    try {
        // Get data from hidden divs with fallback to empty arrays
        const typeData = parseJsonSafely('typeData') || [];
        const locationData = parseJsonSafely('locationData') || [];
        const statusData = parseJsonSafely('statusData') || [];
        
        console.log('Chart data loaded:', {
            typeData: typeData,
            locationData: locationData,
            statusData: statusData
        });

        // Render each chart with error boundaries
        try {
            renderCrimeTypeChart(typeData);
        } catch (e) {
            console.error("Error rendering crime type chart:", e);
            showChartError('crimeTypeChartContainer', 'Crime Type');
        }
        
        try {
            renderLocationChart(locationData);
        } catch (e) {
            console.error("Error rendering location chart:", e);
            showChartError('locationChartContainer', 'Location');
        }
        
        try {
            renderStatusChart(statusData);
        } catch (e) {
            console.error("Error rendering status chart:", e);
            showChartError('statusChartContainer', 'Case Status');
        }
    } catch (error) {
        console.error("Error in renderCharts:", error);
        document.getElementById('analyticsSection').innerHTML = `
            <div class="alert alert-danger">
                Failed to load analytics data. Please try refreshing the page.
            </div>
        `;
    }
}

// Show error message for a specific chart
function showChartError(containerId, chartName) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="chart-error no-data-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load ${chartName} data</p>
            </div>
        `;
    }
}

// Enhanced crime type chart with better tooltips and animations
function renderCrimeTypeChart(typeData) {
    const container = document.getElementById('crimeTypeChartContainer');
    if (!container) return;
    
    let canvas = document.getElementById('crimeTypeChart');
    if (!canvas) {
        container.innerHTML = `
            <div class="chart-title">Crime Type Distribution</div>
            <div class="chart-wrapper">
                <canvas id="crimeTypeChart"></canvas>
            </div>
        `;
        canvas = document.getElementById('crimeTypeChart');
    }
    
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const backgroundColors = [
        'rgba(255, 99, 132, 0.8)',
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 206, 86, 0.8)',
        'rgba(75, 192, 192, 0.8)',
        'rgba(153, 102, 255, 0.8)',
        'rgba(255, 159, 64, 0.8)'
    ];

    const borderColors = backgroundColors.map(color => color.replace('0.8', '1'));
    
    const labels = typeData.map(item => item.incident_type);
    const data = typeData.map(item => item.count);

    if (window.crimeTypeChartInstance) {
        window.crimeTypeChartInstance.destroy();
    }

    if (typeData.length > 0) {
        window.crimeTypeChartInstance = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Crime Distribution by Type',
                        font: { size: 16, weight: 'bold' },
                        padding: { top: 10, bottom: 20 },
                        color: '#333'
                    },
                    legend: {
                        position: 'right',
                        labels: { 
                            boxWidth: 12, 
                            padding: 20, 
                            font: { size: 12 },
                            color: '#333',
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '65%',
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 1500
                }
            }
        });
    } else {
        container.innerHTML = `
            <div class="no-data-message">
                <i class="fas fa-chart-pie"></i>
                <p>No Crime Type data available</p>
            </div>
        `;
    }
}

// Enhanced location chart with better bar styling and fixed text overlap
function renderLocationChart(locationData) {
    const container = document.getElementById('locationChartContainer');
    if (!container) return;
    
    let canvas = document.getElementById('locationChart');
    if (!canvas) {
        container.innerHTML = `
            <div class="chart-title">Top Crime Locations</div>
            <div class="chart-wrapper">
                <canvas id="locationChart"></canvas>
            </div>
        `;
        canvas = document.getElementById('locationChart');
    }
    
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const labels = locationData.map(item => item.location);
    const data = locationData.map(item => item.count);
    
    const backgroundColors = data.map((_, i) => {
        const hue = (i * 360 / data.length) % 360;
        return `hsla(${hue}, 70%, 60%, 0.8)`;
    });

    if (window.locationChartInstance) {
        window.locationChartInstance.destroy();
    }

    if (locationData.length > 0) {
        window.locationChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Number of Reports',
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: backgroundColors.map(color => color.replace('0.8', '1')),
                    borderWidth: 1,
                    borderRadius: 4,
                    hoverBackgroundColor: backgroundColors.map(color => color.replace('0.8', '0.6'))
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y', // Make it horizontal to prevent text overlap
                plugins: {
                    title: {
                        display: true,
                        text: 'Top Crime Locations',
                        font: { size: 16, weight: 'bold' },
                        padding: { top: 10, bottom: 20 },
                        color: '#333'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${context.raw}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { 
                            precision: 0,
                            color: '#666'
                        },
                        title: { 
                            display: true, 
                            text: 'Number of Reports',
                            color: '#666'
                        },
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    y: {
                        ticks: { 
                            color: '#666',
                            autoSkip: false
                        },
                        title: { 
                            display: true, 
                            text: 'Location',
                            color: '#666'
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1500
                }
            }
        });
    } else {
        container.innerHTML = `
            <div class="no-data-message">
                <i class="fas fa-chart-bar"></i>
                <p>No Location data available</p>
            </div>
        `;
    }
}

// Enhanced status chart with better visual hierarchy
function renderStatusChart(statusData) {
    const container = document.getElementById('statusChartContainer');
    if (!container) return;
    
    let canvas = document.getElementById('statusChart');
    if (!canvas) {
        container.innerHTML = `
            <div class="chart-title">Case Status</div>
            <div class="chart-wrapper">
                <canvas id="statusChart"></canvas>
            </div>
        `;
        canvas = document.getElementById('statusChart');
    }
    
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    const labels = statusData.map(item => item.status);
    const data = statusData.map(item => item.count);
    
    const backgroundColors = [
        'rgba(255, 206, 86, 0.8)',   // Pending - yellow
        'rgba(75, 192, 192, 0.8)',   // Received - teal
        'rgba(54, 162, 235, 0.8)',   // In Progress - blue
        'rgba(75, 192, 75, 0.8)'     // Resolved - green
    ];
    
    const borderColors = backgroundColors.map(color => color.replace('0.8', '1'));

    if (window.statusChartInstance) {
        window.statusChartInstance.destroy();
    }

    if (statusData.length > 0) {
        window.statusChartInstance = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 2,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Case Status Distribution',
                        font: { size: 16, weight: 'bold' },
                        padding: { top: 10, bottom: 20 },
                        color: '#333'
                    },
                    legend: {
                        position: 'right',
                        labels: { 
                            boxWidth: 12, 
                            padding: 20, 
                            font: { size: 12 },
                            color: '#333',
                            usePointStyle: true
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateScale: true,
                    animateRotate: true,
                    duration: 1500
                }
            }
        });
    } else {
        container.innerHTML = `
            <div class="no-data-message">
                <i class="fas fa-chart-pie"></i>
                <p>No Status data available</p>
            </div>
        `;
    }
}

// Function to safely parse JSON from hidden div elements
function parseJsonSafely(elementId) {
    const element = document.getElementById(elementId);
    if (element && element.textContent) {
        try {
            return JSON.parse(element.textContent);
        } catch (e) {
            console.error(`Error parsing JSON from ${elementId}:`, e);
            return [];
        }
    }
    return [];
}

// Initialize charts when page loads
if (document.readyState === 'complete') {
    renderCharts();
} else {
    document.addEventListener('DOMContentLoaded', renderCharts);
}