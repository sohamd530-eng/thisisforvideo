/**
 * SurakshaTaap Pune - Chart.js Precision Visualizations
 */

let forecastChartInstance = null;
let workSafeChartInstance = null;

function render5DayForecastChart(canvasId, hourlyData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (forecastChartInstance) {
        forecastChartInstance.destroy();
    }

    const labels = hourlyData.map(h => `${h.hour}:00`);
    const temps = hourlyData.map(h => h.temp_c);
    const wbgts = hourlyData.map(h => h.wbgt_c);
    const utcis = hourlyData.map(h => h.utci_c);

    forecastChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Ambient Dry-Bulb (°C)',
                    data: temps,
                    borderColor: '#64748b',
                    borderDash: [4, 4],
                    backgroundColor: 'transparent',
                    borderWidth: 1.8,
                    pointRadius: 0,
                    pointHoverRadius: 4,
                    tension: 0.25
                },
                {
                    label: 'WBGT Wet-Bulb Globe (°C)',
                    data: wbgts,
                    borderColor: '#f97316',
                    backgroundColor: 'rgba(249, 115, 22, 0.08)',
                    fill: true,
                    borderWidth: 2.2,
                    pointRadius: 1.5,
                    pointHoverRadius: 5,
                    tension: 0.25
                },
                {
                    label: 'UTCI Thermal Strain (°C)',
                    data: utcis,
                    borderColor: '#ef4444',
                    backgroundColor: 'transparent',
                    borderWidth: 2.2,
                    pointRadius: 1.5,
                    pointHoverRadius: 5,
                    tension: 0.25
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false
            },
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        color: '#94a3b8',
                        font: { size: 10, family: 'JetBrains Mono' },
                        boxWidth: 12,
                        boxHeight: 2
                    }
                },
                tooltip: {
                    backgroundColor: '#0f1523',
                    titleColor: '#38bdf8',
                    bodyColor: '#f8fafc',
                    borderColor: '#243350',
                    borderWidth: 1,
                    padding: 8,
                    titleFont: { family: 'JetBrains Mono', size: 11 },
                    bodyFont: { family: 'JetBrains Mono', size: 10 }
                }
            },
            scales: {
                x: {
                    grid: { color: '#131c31' },
                    ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 12 }
                },
                y: {
                    grid: { color: '#131c31' },
                    ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 } }
                }
            }
        }
    });
}

function renderSafeWorkChart(canvasId, hourlyData) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    if (workSafeChartInstance) {
        workSafeChartInstance.destroy();
    }

    const labels = hourlyData.map(h => `${h.hour}:00`);
    const safeMins = hourlyData.map(h => h.safe_work_mins);

    workSafeChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Safe Labor (Mins/Hr)',
                data: safeMins,
                backgroundColor: safeMins.map(m => {
                    if (m === 0) return '#e11d48';
                    if (m <= 15) return '#ef4444';
                    if (m <= 30) return '#f97316';
                    if (m <= 60) return '#f59e0b';
                    return '#10b981';
                }),
                borderRadius: 2,
                barPercentage: 0.75
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#0f1523',
                    titleColor: '#38bdf8',
                    bodyColor: '#f8fafc',
                    borderColor: '#243350',
                    borderWidth: 1,
                    padding: 8,
                    titleFont: { family: 'JetBrains Mono', size: 11 },
                    bodyFont: { family: 'JetBrains Mono', size: 10 }
                }
            },
            scales: {
                x: {
                    grid: { color: '#131c31' },
                    ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 }, maxTicksLimit: 8 }
                },
                y: {
                    grid: { color: '#131c31' },
                    ticks: { color: '#64748b', font: { family: 'JetBrains Mono', size: 9 } },
                    max: 120
                }
            }
        }
    });
}
