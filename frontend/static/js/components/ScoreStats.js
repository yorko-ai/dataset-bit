class ScoreStats {
    constructor(container, options = {}) {
        this.container = container;
        this.lang = options.lang || 'zh';
        this.theme = options.theme || 'light';
        this.translations = this.getTranslations();
        this.themeConfig = this.getThemeConfig();
        
        this.init();
    }
    
    getTranslations() {
        return {
            zh: {
                title: '评分统计',
                trend: '评分趋势',
                distribution: '评分分布',
                total: '总分',
                accuracy: '准确性',
                completeness: '完整性',
                relevance: '相关性',
                clarity: '清晰度',
                date: '日期',
                score: '分数',
                count: '数量',
                range: '分数范围',
                noData: '暂无数据'
            },
            en: {
                title: 'Score Statistics',
                trend: 'Score Trend',
                distribution: 'Score Distribution',
                total: 'Total',
                accuracy: 'Accuracy',
                completeness: 'Completeness',
                relevance: 'Relevance',
                clarity: 'Clarity',
                date: 'Date',
                score: 'Score',
                count: 'Count',
                range: 'Score Range',
                noData: 'No Data'
            }
        }[this.lang];
    }
    
    getThemeConfig() {
        return {
            light: {
                backgroundColor: '#ffffff',
                textColor: '#333333',
                gridColor: '#e0e0e0',
                borderColor: '#dddddd',
                colors: ['#4a90e2', '#28a745', '#ffc107', '#dc3545', '#6c757d']
            },
            dark: {
                backgroundColor: '#2d2d2d',
                textColor: '#ffffff',
                gridColor: '#4d4d4d',
                borderColor: '#3d3d3d',
                colors: ['#4a90e2', '#28a745', '#ffc107', '#dc3545', '#6c757d']
            }
        }[this.theme];
    }
    
    init() {
        this.container.innerHTML = `
            <div class="score-stats">
                <h2>${this.translations.title}</h2>
                <div class="stats-container">
                    <div class="trend-chart">
                        <h3>${this.translations.trend}</h3>
                        <canvas id="trendChart"></canvas>
                    </div>
                    <div class="distribution-chart">
                        <h3>${this.translations.distribution}</h3>
                        <canvas id="distributionChart"></canvas>
                    </div>
                </div>
            </div>
        `;
        
        this.trendChart = new Chart(
            document.getElementById('trendChart'),
            this.getTrendChartConfig()
        );
        
        this.distributionChart = new Chart(
            document.getElementById('distributionChart'),
            this.getDistributionChartConfig()
        );
    }
    
    getTrendChartConfig() {
        return {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: this.translations.total,
                        data: [],
                        borderColor: this.themeConfig.colors[0],
                        tension: 0.1
                    },
                    {
                        label: this.translations.accuracy,
                        data: [],
                        borderColor: this.themeConfig.colors[1],
                        tension: 0.1
                    },
                    {
                        label: this.translations.completeness,
                        data: [],
                        borderColor: this.themeConfig.colors[2],
                        tension: 0.1
                    },
                    {
                        label: this.translations.relevance,
                        data: [],
                        borderColor: this.themeConfig.colors[3],
                        tension: 0.1
                    },
                    {
                        label: this.translations.clarity,
                        data: [],
                        borderColor: this.themeConfig.colors[4],
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: this.themeConfig.textColor
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    },
                    y: {
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    }
                }
            }
        };
    }
    
    getDistributionChartConfig() {
        return {
            type: 'bar',
            data: {
                labels: ['0-20', '21-40', '41-60', '61-80', '81-100'],
                datasets: [
                    {
                        label: this.translations.total,
                        data: [],
                        backgroundColor: this.themeConfig.colors[0]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            color: this.themeConfig.textColor
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    },
                    y: {
                        grid: {
                            color: this.themeConfig.gridColor
                        },
                        ticks: {
                            color: this.themeConfig.textColor
                        }
                    }
                }
            }
        };
    }
    
    updateData(history) {
        if (!history || history.length === 0) {
            this.trendChart.data.labels = [];
            this.trendChart.data.datasets.forEach(dataset => dataset.data = []);
            this.distributionChart.data.datasets[0].data = [0, 0, 0, 0, 0];
            this.trendChart.update();
            this.distributionChart.update();
            return;
        }
        
        // 更新趋势图数据
        const dates = history.map(h => new Date(h.created_at).toLocaleDateString());
        const totalScores = history.map(h => h.total_score);
        const accuracyScores = history.map(h => h.accuracy_score);
        const completenessScores = history.map(h => h.completeness_score);
        const relevanceScores = history.map(h => h.relevance_score);
        const clarityScores = history.map(h => h.clarity_score);
        
        this.trendChart.data.labels = dates;
        this.trendChart.data.datasets[0].data = totalScores;
        this.trendChart.data.datasets[1].data = accuracyScores;
        this.trendChart.data.datasets[2].data = completenessScores;
        this.trendChart.data.datasets[3].data = relevanceScores;
        this.trendChart.data.datasets[4].data = clarityScores;
        
        // 更新分布图数据
        const distribution = [0, 0, 0, 0, 0];
        totalScores.forEach(score => {
            const index = Math.floor(score / 20);
            if (index >= 0 && index < 5) {
                distribution[index]++;
            }
        });
        
        this.distributionChart.data.datasets[0].data = distribution;
        
        this.trendChart.update();
        this.distributionChart.update();
    }
    
    updateLang(lang) {
        this.lang = lang;
        this.translations = this.getTranslations();
        
        // 更新图表标签
        this.trendChart.data.datasets[0].label = this.translations.total;
        this.trendChart.data.datasets[1].label = this.translations.accuracy;
        this.trendChart.data.datasets[2].label = this.translations.completeness;
        this.trendChart.data.datasets[3].label = this.translations.relevance;
        this.trendChart.data.datasets[4].label = this.translations.clarity;
        
        this.distributionChart.data.datasets[0].label = this.translations.total;
        
        this.trendChart.update();
        this.distributionChart.update();
    }
    
    updateTheme(theme) {
        this.theme = theme;
        this.themeConfig = this.getThemeConfig();
        
        // 更新图表主题
        this.trendChart.options.scales.x.grid.color = this.themeConfig.gridColor;
        this.trendChart.options.scales.y.grid.color = this.themeConfig.gridColor;
        this.trendChart.options.scales.x.ticks.color = this.themeConfig.textColor;
        this.trendChart.options.scales.y.ticks.color = this.themeConfig.textColor;
        this.trendChart.options.plugins.legend.labels.color = this.themeConfig.textColor;
        
        this.distributionChart.options.scales.x.grid.color = this.themeConfig.gridColor;
        this.distributionChart.options.scales.y.grid.color = this.themeConfig.gridColor;
        this.distributionChart.options.scales.x.ticks.color = this.themeConfig.textColor;
        this.distributionChart.options.scales.y.ticks.color = this.themeConfig.textColor;
        this.distributionChart.options.plugins.legend.labels.color = this.themeConfig.textColor;
        
        this.trendChart.update();
        this.distributionChart.update();
    }
} 