// Dashboard Charts Initialization
function initDashboardCharts(labels, data) {
    // Status chart
    const statusCtx = document.getElementById('statusChart')?.getContext('2d');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#ffc107', // Pending
                        '#0dcaf0', // Received
                        '#fd7e14', // Under Investigation
                        '#198754'  // Resolved
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Report modal functions
function viewReport(reportId) {
    fetch(`/admin/get_report/${reportId}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            if (!data) throw new Error('No data received');
            
            document.getElementById('reportId').textContent = data.id;
            document.getElementById('modalReportId').value = data.id;
            document.getElementById('reportUser').textContent = `${data.fname} ${data.lname} (${data.email})`;
            document.getElementById('reportContact').textContent = data.phone_num || 'N/A';
            document.getElementById('reportLocation').innerHTML = 
                `<a href="https://www.google.com/maps?q=${data.latitude},${data.longitude}" target="_blank">${data.location}</a>`;
            document.getElementById('reportDate').textContent = data.report_date;
            document.getElementById('reportStatus').innerHTML = 
                `<span class="status-badge status-${data.status.toLowerCase().replace(' ', '-')}">${data.status}</span>`;
            document.getElementById('reportConcern').textContent = data.concern;
            document.getElementById('statusUpdate').value = data.status;
            document.getElementById('adminFeedback').value = data.admin_feedback || '';
            
            const modal = new bootstrap.Modal(document.getElementById('reportModal'));
            modal.show();
        })
        .catch(error => {
            console.error('Error fetching report:', error);
            alert('Failed to load report details. Please try again.');
        });
}

// Initialize form submission for status updates
document.addEventListener('DOMContentLoaded', function() {
    const statusForm = document.getElementById('statusForm');
    if (statusForm) {
        statusForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const reportId = document.getElementById('modalReportId').value;
            const status = document.getElementById('statusUpdate').value;
            const feedback = document.getElementById('adminFeedback').value;
            
            fetch(`/admin/update_report_status/${reportId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `status=${encodeURIComponent(status)}&feedback=${encodeURIComponent(feedback)}`
            })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    throw new Error('Failed to update status');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to update report status. Please try again.');
            });
        });
    }
});

// Analysis page functions
function initAnalysisCharts(typeData, statusData, trendData) {
    // Crime Type Distribution Chart
    const typeCtx = document.getElementById('typeChart')?.getContext('2d');
    if (typeCtx) {
        new Chart(typeCtx, {
            type: 'bar',
            data: {
                labels: typeData.map(item => item.incident_type),
                datasets: [{
                    label: 'Number of Reports',
                    data: typeData.map(item => item.count),
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Status Distribution Chart
    const statusCtx = document.getElementById('statusChart')?.getContext('2d');
    if (statusCtx) {
        new Chart(statusCtx, {
            type: 'pie',
            data: {
                labels: statusData.map(item => item.status),
                datasets: [{
                    data: statusData.map(item => item.count),
                    backgroundColor: [
                        '#ffc107', // Pending
                        '#0dcaf0', // Received
                        '#fd7e14', // Under Investigation
                        '#198754'  // Resolved
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // Monthly Trend Chart
    const trendCtx = document.getElementById('trendChart')?.getContext('2d');
    if (trendCtx) {
        new Chart(trendCtx, {
            type: 'line',
            data: {
                labels: trendData.map(item => item.month),
                datasets: [{
                    label: 'Reports per Month',
                    data: trendData.map(item => item.count),
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Heatmap functions
function initHeatmap(heatmapData) {
    const heatmapElement = document.getElementById('heatmap');
    if (!heatmapElement) return;

    const map = L.map('heatmap').setView([10.6747, 122.3766], 13)
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add markers for each crime location
    heatmapData.forEach(item => {
        if (item.latitude && item.longitude) {
            const radius = Math.min(item.count * 2, 30);
            const color = getColorForCrimeType(item.incident_type);
            
            L.circleMarker([item.latitude, item.longitude], {
                radius: radius,
                fillColor: color,
                color: '#fff',
                weight: 1,
                opacity: 1,
                fillOpacity: 0.7
            }).addTo(map).bindPopup(`
                <b>${item.incident_type}</b><br>
                Reports: ${item.count}<br>
                Location: ${item.location || 'N/A'}
            `);
        }
    });

    // Zoom to Iloilo function
    window.zoomToIloilo = function() {
        map.setView([10.6747, 122.3766], 13)
    };
}

function getColorForCrimeType(type) {
    const colors = {
        'Theft': '#ff6384',
        'Rape': '#36a2eb',
        'Vehicular Accident': '#ffce56',
        'Murder': '#4bc0c0',
        'Fraud': '#9966ff',
        'Other': '#ff9f40'
    };
    return colors[type] || '#cccccc';
}

// Logs page functions
function showDetails(details) {
    const modal = new bootstrap.Modal(document.getElementById('detailsModal'));
    document.getElementById('detailsContent').textContent = JSON.stringify(details, null, 2);
    modal.show();
}

function blockUser(userId, userName) {
    currentUserIdToBlock = userId;
    const modal = new bootstrap.Modal(document.getElementById('blockUserModal'));
    document.getElementById('blockUserMessage').textContent = `Are you sure you want to block ${userName}?`;
    document.getElementById('blockReason').value = '';
    modal.show();
}

function unblockUser(userId, userName) {
    if (confirm(`Are you sure you want to unblock ${userName}?`)) {
        fetch(`/admin/unblock_user/${userId}`)
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    throw new Error('Failed to unblock user');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to unblock user. Please try again.');
            });
    }
}

// Settings page functions
function confirmDeleteAdmin(adminId, username) {
    adminToDelete = adminId;
    const modal = new bootstrap.Modal(document.getElementById('deleteAdminModal'));
    document.getElementById('deleteAdminMessage').textContent = `Are you sure you want to delete admin account "${username}"?`;
    modal.show();
}

function editAdmin(adminId) {
    // In a real implementation, this would open an edit modal
    alert('Edit admin with ID: ' + adminId);
}

// Initialize event listeners for logs page
document.addEventListener('DOMContentLoaded', function() {
    // Confirm block button
    const confirmBlockBtn = document.getElementById('confirmBlock');
    if (confirmBlockBtn) {
        confirmBlockBtn.addEventListener('click', function() {
            if (currentUserIdToBlock) {
                const reason = document.getElementById('blockReason').value;
                
                fetch(`/admin/block_user/${currentUserIdToBlock}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `reason=${encodeURIComponent(reason)}`
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        throw new Error('Failed to block user');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to block user. Please try again.');
                });
            }
        });
    }

    // Confirm delete admin button
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', function() {
            if (adminToDelete) {
                fetch(`/admin/delete_admin/${adminToDelete}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        throw new Error('Failed to delete admin');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to delete admin. Please try again.');
                });
            }
        });
    }

    // Time filter change
    const timeFilter = document.getElementById('timeFilter');
    if (timeFilter) {
        timeFilter.addEventListener('change', function() {
            const timeRange = this.value;
            fetchFilteredData(timeRange);
        });
    }
});

function fetchFilteredData(timeRange) {
    // In a real implementation, this would fetch data based on the time filter
    console.log('Fetching data for time range:', timeRange);
    // You would typically make an AJAX call here to get filtered data
    // and then update the charts/tables
}

// Download chart as image
function downloadChart(chartId) {
    const canvas = document.getElementById(chartId);
    if (!canvas) return;
    
    const link = document.createElement('a');
    link.download = `${chartId}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
}