class ScoreChart {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            lang: options.lang || 'zh',
            theme: options.theme || 'light',
            scores: options.scores || {},
            type: options.type || 'radar' // radar, bar, line
        };
        
        this.translations = {
            zh: {
                accuracy: '准确性',
                completeness: '完整性',
                relevance: '相关性',
                clarity: '清晰度',
                total: '总分',
                score: '得分'
            },
            en: {
                accuracy: 'Accuracy',
                completeness: 'Completeness',
                relevance: 'Relevance',
                clarity: 'Clarity',
                total: 'Total',
                score: 'Score'
            }
        };
        
        this.themes = {
            light: {
                background: '#ffffff',
                text: '#333333',
                grid: '#e0e0e0',
                point: '#4a90e2',
                line: '#4a90e2',
                fill: 'rgba(74, 144, 226, 0.2)'
            },
            dark: {
                background: '#2d2d2d',
                text: '#ffffff',
                grid: '#404040',
                point: '#64b5f6',
                line: '#64b5f6',
                fill: 'rgba(100, 181, 246, 0.2)'
            }
        };
        
        this.chart = null;
        this.render();
    }
    
    render() {
        const t = this.translations[this.options.lang];
        const theme = this.themes[this.options.theme];
        
        // 准备数据
        const labels = [
            t.accuracy,
            t.completeness,
            t.relevance,
            t.clarity,
            t.total
        ];
        
        const data = [
            this.options.scores.accuracy || 0,
            this.options.scores.completeness || 0,
            this.options.scores.relevance || 0,
            this.options.scores.clarity || 0,
            this.options.scores.total || 0
        ];
        
        // 创建canvas
        this.container.innerHTML = '<canvas></canvas>';
        const ctx = this.container.querySelector('canvas').getContext('2d');
        
        // 配置图表
        const config = {
            type: this.options.type,
            data: {
                labels: labels,
                datasets: [{
                    label: t.score,
                    data: data,
                    backgroundColor: theme.fill,
                    borderColor: theme.line,
                    pointBackgroundColor: theme.point,
                    pointBorderColor: theme.point,
                    pointHoverBackgroundColor: theme.point,
                    pointHoverBorderColor: theme.point
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            stepSize: 0.2,
                            color: theme.text
                        },
                        grid: {
                            color: theme.grid
                        },
                        pointLabels: {
                            color: theme.text
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: theme.text
                        }
                    }
                }
            }
        };
        
        // 创建图表
        if (this.chart) {
            this.chart.destroy();
        }
        this.chart = new Chart(ctx, config);
    }
    
    updateScores(scores) {
        this.options.scores = scores;
        this.render();
    }
    
    updateLang(lang) {
        this.options.lang = lang;
        this.render();
    }
    
    updateTheme(theme) {
        this.options.theme = theme;
        this.render();
    }
    
    updateType(type) {
        this.options.type = type;
        this.render();
    }
} 