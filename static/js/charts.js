/**
 * Smart Student Complaint Analyzer - Dynamic Chart.js Visualizations
 */

// Color Palette
const CHART_COLORS = {
    primary: '#2563EB',
    primaryLight: '#93C5FD',
    success: '#16A34A',
    warning: '#F59E0B',
    danger: '#DC2626',
    info: '#0284C7',
    neutral: '#94A3B8',
    purple: '#9333EA',
    teal: '#0D9488',
    pink: '#DB2777',
    orange: '#EA580C',
    indigo: '#4F46E5',
    palette: [
        '#2563EB', '#0D9488', '#F59E0B', '#DC2626', '#9333EA', 
        '#0284C7', '#16A34A', '#EA580C', '#4F46E5', '#64748B',
        '#DB2777', '#84CC16'
    ]
};

function initCategoryChart(canvasId, categoryData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !categoryData) return;

    const labels = Object.keys(categoryData);
    const counts = Object.values(categoryData);

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Complaints',
                data: counts,
                backgroundColor: CHART_COLORS.palette.slice(0, labels.length),
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                },
                x: {
                    ticks: { autoSkip: false, maxRotation: 45, minRotation: 45 }
                }
            }
        }
    });
}

function initSentimentChart(canvasId, sentimentData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !sentimentData) return;

    const labels = ['Positive', 'Neutral', 'Negative'];
    const counts = [
        sentimentData['Positive'] || 0,
        sentimentData['Neutral'] || 0,
        sentimentData['Negative'] || 0
    ];

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: [CHART_COLORS.success, CHART_COLORS.neutral, CHART_COLORS.danger],
                borderWidth: 2,
                borderColor: '#FFFFFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            },
            cutout: '65%'
        }
    });
}

function initPriorityChart(canvasId, priorityData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !priorityData) return;

    const labels = ['High', 'Medium', 'Low'];
    const counts = [
        priorityData['High'] || 0,
        priorityData['Medium'] || 0,
        priorityData['Low'] || 0
    ];

    new Chart(canvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: [CHART_COLORS.danger, CHART_COLORS.warning, '#CBD5E1'],
                borderWidth: 2,
                borderColor: '#FFFFFF'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}

function initStatusChart(canvasId, statusData) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !statusData) return;

    const labels = ['Pending', 'In Progress', 'Resolved', 'Rejected'];
    const counts = [
        statusData['Pending'] || 0,
        statusData['In Progress'] || 0,
        statusData['Resolved'] || 0,
        statusData['Rejected'] || 0
    ];

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Status Count',
                data: counts,
                backgroundColor: [
                    CHART_COLORS.warning,
                    CHART_COLORS.info,
                    CHART_COLORS.success,
                    CHART_COLORS.danger
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });
}
