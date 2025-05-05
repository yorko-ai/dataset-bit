class AdvancedCharts {
    constructor(container, options = {}) {
        this.container = container;
        this.lang = options.lang || 'zh';
        this.theme = options.theme || 'light';
        this.translations = this.getTranslations();
        this.themeConfig = this.getThemeConfig();
        this.charts = {};
        
        this.init();
    }
    
    getTranslations() {
        return {
            zh: {
                radarChart: '雷达图',
                scatterChart: '散点图',
                heatmapChart: '热力图',
                accuracy: '准确性',
                completeness: '完整性',
                relevance: '相关性',
                clarity: '清晰度',
                total: '总分',
                date: '日期',
                score: '分数',
                noData: '暂无数据'
            },
            en: {
                radarChart: 'Radar Chart',
                scatterChart: 'Scatter Chart',
                heatmapChart: 'Heatmap',
                accuracy: 'Accuracy',
                completeness: 'Completeness',
                relevance: 'Relevance',
                clarity: 'Clarity',
                total: 'Total',
                date: 'Date',
                score: 'Score',
                noData: 'No Data'
            }
        }[this.lang];
    }
    
    getThemeConfig() {
        return {
            light: {
                backgroundColor: '#ffffff',
                textColor: '#333333',
                borderColor: '#dddddd',
                gridColor: '#eeeeee',
                chartColors: [
                    '#4a90e2',
                    '#50e3c2',
                    '#f5a623',
                    '#d0021b',
                    '#9013fe'
                ]
            },
            dark: {
                backgroundColor: '#2d2d2d',
                textColor: '#ffffff',
                borderColor: '#3d3d3d',
                gridColor: '#3d3d3d',
                chartColors: [
                    '#4a90e2',
                    '#50e3c2',
                    '#f5a623',
                    '#d0021b',
                    '#9013fe'
                ]
            }
        }[this.theme];
    }
    
    init() {
        this.container.innerHTML = `
            <div class="advanced-charts">
                <div class="chart-tabs">
                    <button class="btn" data-chart="radar">${this.translations.radarChart}</button>
                    <button class="btn" data-chart="scatter">${this.translations.scatterChart}</button>
                    <button class="btn" data-chart="heatmap">${this.translations.heatmapChart}</button>
                </div>
                <div class="chart-container">
                    <canvas id="radarChart"></canvas>
                    <canvas id="scatterChart"></canvas>
                    <canvas id="heatmapChart"></canvas>
                </div>
            </div>
        `;
        
        this.applyStyles();
        this.initCharts();
        this.bindEvents();
    }
    
    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .advanced-charts {
                background-color: ${this.themeConfig.backgroundColor};
                border: 1px solid ${this.themeConfig.borderColor};
                border-radius: 4px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .chart-tabs {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            
            .chart-container {
                position: relative;
                height: 400px;
            }
            
            .chart-container canvas {
                display: none;
                width: 100% !important;
                height: 100% !important;
            }
            
            .chart-container canvas.active {
                display: block;
            }
            
            .btn {
                padding: 8px 16px;
                border: 1px solid ${this.themeConfig.borderColor};
                border-radius: 4px;
                background-color: ${this.themeConfig.backgroundColor};
                color: ${this.themeConfig.textColor};
                cursor: pointer;
            }
            
            .btn:hover {
                background-color: ${this.themeConfig.gridColor};
            }
            
            .btn.active {
                background-color: ${this.themeConfig.chartColors[0]};
                color: #ffffff;
                border-color: ${this.themeConfig.chartColors[0]};
            }
        `;
        document.head.appendChild(style);
    }
    
    initCharts() {
        // 初始化雷达图
        const radarCtx = document.getElementById('radarChart').getContext('2d');
        this.charts.radar = new Chart(radarCtx, {
            type: 'radar',
            data: {
                labels: [
                    this.translations.accuracy,
                    this.translations.completeness,
                    this.translations.relevance,
                    this.translations.clarity,
                    this.translations.total
                ],
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            color: this.themeConfig.textColor
                        },
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        pointLabels: {
                            color: this.themeConfig.textColor
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: this.themeConfig.textColor
                        }
                    }
                }
            }
        });
        
        // 初始化散点图
        const scatterCtx = document.getElementById('scatterChart').getContext('2d');
        this.charts.scatter = new Chart(scatterCtx, {
            type: 'scatter',
            data: {
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        title: {
                            display: true,
                            text: this.translations.date,
                            color: this.themeConfig.textColor
                        },
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: this.translations.score,
                            color: this.themeConfig.textColor
                        },
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: this.themeConfig.textColor
                        }
                    }
                }
            }
        });
        
        // 初始化热力图
        const heatmapCtx = document.getElementById('heatmapChart').getContext('2d');
        this.charts.heatmap = new Chart(heatmapCtx, {
            type: 'matrix',
            data: {
                datasets: []
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'category',
                        labels: [
                            this.translations.accuracy,
                            this.translations.completeness,
                            this.translations.relevance,
                            this.translations.clarity,
                            this.translations.total
                        ],
                        title: {
                            display: true,
                            text: this.translations.score,
                            color: this.themeConfig.textColor
                        },
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    },
                    y: {
                        type: 'category',
                        labels: [],
                        title: {
                            display: true,
                            text: this.translations.date,
                            color: this.themeConfig.textColor
                        },
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `${context.dataset.label}: ${context.raw.v}`;
                            }
                        }
                    }
                }
            }
        });
        
        // 默认显示雷达图
        document.getElementById('radarChart').classList.add('active');
        document.querySelector('[data-chart="radar"]').classList.add('active');
    }
    
    bindEvents() {
        const tabs = this.container.querySelectorAll('.chart-tabs button');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // 更新按钮状态
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                // 更新图表显示
                const chartType = tab.dataset.chart;
                const canvases = this.container.querySelectorAll('canvas');
                canvases.forEach(canvas => canvas.classList.remove('active'));
                document.getElementById(`${chartType}Chart`).classList.add('active');
            });
        });
    }
    
    updateData(data) {
        if (!data || data.length === 0) {
            this.showNoData();
            return;
        }
        
        // 更新雷达图
        this.updateRadarChart(data);
        
        // 更新散点图
        this.updateScatterChart(data);
        
        // 更新热力图
        this.updateHeatmapChart(data);
    }
    
    updateRadarChart(data) {
        const datasets = data.map((item, index) => ({
            label: `${this.translations.total} ${index + 1}`,
            data: [
                item.accuracy_score,
                item.completeness_score,
                item.relevance_score,
                item.clarity_score,
                item.total_score
            ],
            backgroundColor: this.themeConfig.chartColors[index % this.themeConfig.chartColors.length] + '40',
            borderColor: this.themeConfig.chartColors[index % this.themeConfig.chartColors.length],
            borderWidth: 2
        }));
        
        this.charts.radar.data.datasets = datasets;
        this.charts.radar.update();
    }
    
    updateScatterChart(data) {
        const datasets = [
            {
                label: this.translations.accuracy,
                data: data.map(item => ({
                    x: new Date(item.created_at),
                    y: item.accuracy_score
                })),
                backgroundColor: this.themeConfig.chartColors[0]
            },
            {
                label: this.translations.completeness,
                data: data.map(item => ({
                    x: new Date(item.created_at),
                    y: item.completeness_score
                })),
                backgroundColor: this.themeConfig.chartColors[1]
            },
            {
                label: this.translations.relevance,
                data: data.map(item => ({
                    x: new Date(item.created_at),
                    y: item.relevance_score
                })),
                backgroundColor: this.themeConfig.chartColors[2]
            },
            {
                label: this.translations.clarity,
                data: data.map(item => ({
                    x: new Date(item.created_at),
                    y: item.clarity_score
                })),
                backgroundColor: this.themeConfig.chartColors[3]
            },
            {
                label: this.translations.total,
                data: data.map(item => ({
                    x: new Date(item.created_at),
                    y: item.total_score
                })),
                backgroundColor: this.themeConfig.chartColors[4]
            }
        ];
        
        this.charts.scatter.data.datasets = datasets;
        this.charts.scatter.update();
    }
    
    updateHeatmapChart(data) {
        // 准备数据
        const dates = [...new Set(data.map(item => item.created_at.split(' ')[0]))].sort();
        const scores = [
            this.translations.accuracy,
            this.translations.completeness,
            this.translations.relevance,
            this.translations.clarity,
            this.translations.total
        ];
        
        // 更新Y轴标签
        this.charts.heatmap.options.scales.y.labels = dates;
        
        // 准备数据集
        const datasets = scores.map((score, scoreIndex) => ({
            label: score,
            data: dates.map((date, dateIndex) => {
                const item = data.find(d => d.created_at.startsWith(date));
                if (!item) return null;
                
                const value = [
                    item.accuracy_score,
                    item.completeness_score,
                    item.relevance_score,
                    item.clarity_score,
                    item.total_score
                ][scoreIndex];
                
                return {
                    x: scoreIndex,
                    y: dateIndex,
                    v: value
                };
            }).filter(Boolean),
            backgroundColor: (context) => {
                const value = context.dataset.data[context.dataIndex].v;
                const alpha = value / 100;
                return this.themeConfig.chartColors[scoreIndex] + Math.round(alpha * 255).toString(16).padStart(2, '0');
            },
            borderColor: this.themeConfig.chartColors[scoreIndex],
            borderWidth: 1,
            width: ({ chart }) => (chart.chartArea || {}).width / scores.length - 1,
            height: ({ chart }) => (chart.chartArea || {}).height / dates.length - 1
        }));
        
        this.charts.heatmap.data.datasets = datasets;
        this.charts.heatmap.update();
    }
    
    showNoData() {
        const canvases = this.container.querySelectorAll('canvas');
        canvases.forEach(canvas => {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = this.themeConfig.textColor;
            ctx.font = '16px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.translations.noData, canvas.width / 2, canvas.height / 2);
        });
    }
    
    updateLang(lang) {
        this.lang = lang;
        this.translations = this.getTranslations();
        this.init();
    }
    
    updateTheme(theme) {
        this.theme = theme;
        this.themeConfig = this.getThemeConfig();
        this.init();
    }
} 