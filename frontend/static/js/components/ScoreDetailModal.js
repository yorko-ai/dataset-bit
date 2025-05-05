class ScoreDetailModal {
    constructor(container, options = {}) {
        this.container = container;
        this.options = {
            lang: options.lang || 'zh',
            theme: options.theme || 'light',
            ...options
        };
        
        this.translations = {
            zh: {
                title: '评分详情',
                accuracy: '准确性',
                completeness: '完整性',
                relevance: '相关性',
                clarity: '清晰度',
                total: '总分',
                history: '历史记录',
                current: '当前评分',
                date: '评分时间',
                no_history: '暂无历史记录',
                close: '关闭'
            },
            en: {
                title: 'Score Details',
                accuracy: 'Accuracy',
                completeness: 'Completeness',
                relevance: 'Relevance',
                clarity: 'Clarity',
                total: 'Total',
                history: 'History',
                current: 'Current Score',
                date: 'Score Time',
                no_history: 'No History',
                close: 'Close'
            }
        };
        
        this.themes = {
            light: {
                background: '#ffffff',
                text: '#333333',
                border: '#dddddd',
                header: '#f5f5f5',
                hover: '#f0f0f0'
            },
            dark: {
                background: '#2d2d2d',
                text: '#ffffff',
                border: '#404040',
                header: '#363636',
                hover: '#404040'
            }
        };
        
        this.init();
    }
    
    init() {
        this.render();
        this.bindEvents();
    }
    
    render() {
        const t = this.translations[this.options.lang];
        const theme = this.themes[this.options.theme];
        
        const modal = document.createElement('div');
        modal.className = 'score-detail-modal';
        modal.style.cssText = `
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        `;
        
        const content = document.createElement('div');
        content.className = 'score-detail-content';
        content.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: ${theme.background};
            border: 1px solid ${theme.border};
            border-radius: 8px;
            padding: 20px;
            width: 80%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
        `;
        
        const header = document.createElement('div');
        header.className = 'score-detail-header';
        header.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid ${theme.border};
        `;
        
        const title = document.createElement('h2');
        title.textContent = t.title;
        title.style.cssText = `
            margin: 0;
            color: ${theme.text};
            font-size: 1.5em;
        `;
        
        const closeBtn = document.createElement('button');
        closeBtn.textContent = t.close;
        closeBtn.className = 'btn';
        closeBtn.style.cssText = `
            background: none;
            border: 1px solid ${theme.border};
            color: ${theme.text};
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
        `;
        
        header.appendChild(title);
        header.appendChild(closeBtn);
        
        const body = document.createElement('div');
        body.className = 'score-detail-body';
        
        const currentScore = document.createElement('div');
        currentScore.className = 'current-score';
        currentScore.innerHTML = `
            <h3 style="color: ${theme.text}">${t.current}</h3>
            <div class="score-details" style="margin-bottom: 20px;">
                <div class="score-item">
                    <span style="color: ${theme.text}">${t.accuracy}:</span>
                    <span class="accuracy-score">-</span>
                </div>
                <div class="score-item">
                    <span style="color: ${theme.text}">${t.completeness}:</span>
                    <span class="completeness-score">-</span>
                </div>
                <div class="score-item">
                    <span style="color: ${theme.text}">${t.relevance}:</span>
                    <span class="relevance-score">-</span>
                </div>
                <div class="score-item">
                    <span style="color: ${theme.text}">${t.clarity}:</span>
                    <span class="clarity-score">-</span>
                </div>
                <div class="score-item">
                    <span style="color: ${theme.text}">${t.total}:</span>
                    <span class="total-score">-</span>
                </div>
            </div>
        `;
        
        const history = document.createElement('div');
        history.className = 'score-history';
        history.innerHTML = `
            <h3 style="color: ${theme.text}">${t.history}</h3>
            <div class="history-list" style="max-height: 300px; overflow-y: auto;">
                <div class="no-history" style="color: ${theme.text}; text-align: center; padding: 20px;">
                    ${t.no_history}
                </div>
            </div>
        `;
        
        body.appendChild(currentScore);
        body.appendChild(history);
        
        content.appendChild(header);
        content.appendChild(body);
        modal.appendChild(content);
        
        this.container.appendChild(modal);
        this.modal = modal;
        this.content = content;
        this.closeBtn = closeBtn;
        this.historyList = history.querySelector('.history-list');
    }
    
    bindEvents() {
        this.closeBtn.addEventListener('click', () => this.hide());
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.hide();
            }
        });
    }
    
    show(scores, history = []) {
        const t = this.translations[this.options.lang];
        const theme = this.themes[this.options.theme];
        
        // 更新当前评分
        this.content.querySelector('.accuracy-score').textContent = scores.accuracy_score.toFixed(2);
        this.content.querySelector('.completeness-score').textContent = scores.completeness_score.toFixed(2);
        this.content.querySelector('.relevance-score').textContent = scores.relevance_score.toFixed(2);
        this.content.querySelector('.clarity-score').textContent = scores.clarity_score.toFixed(2);
        this.content.querySelector('.total-score').textContent = scores.total_score.toFixed(2);
        
        // 更新历史记录
        if (history.length > 0) {
            this.historyList.innerHTML = history.map(record => `
                <div class="history-item" style="
                    padding: 10px;
                    border-bottom: 1px solid ${theme.border};
                    color: ${theme.text};
                ">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span>${t.date}: ${new Date(record.created_at).toLocaleString()}</span>
                        <span>${t.total}: ${record.total_score.toFixed(2)}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                        <div>${t.accuracy}: ${record.accuracy_score.toFixed(2)}</div>
                        <div>${t.completeness}: ${record.completeness_score.toFixed(2)}</div>
                        <div>${t.relevance}: ${record.relevance_score.toFixed(2)}</div>
                        <div>${t.clarity}: ${record.clarity_score.toFixed(2)}</div>
                    </div>
                    ${record.feedback ? `<div style="margin-top: 5px; font-style: italic;">${record.feedback}</div>` : ''}
                </div>
            `).join('');
        } else {
            this.historyList.innerHTML = `
                <div class="no-history" style="color: ${theme.text}; text-align: center; padding: 20px;">
                    ${t.no_history}
                </div>
            `;
        }
        
        this.modal.style.display = 'block';
    }
    
    hide() {
        this.modal.style.display = 'none';
    }
    
    updateLang(lang) {
        this.options.lang = lang;
        const t = this.translations[lang];
        
        this.content.querySelector('h2').textContent = t.title;
        this.closeBtn.textContent = t.close;
        
        const currentScore = this.content.querySelector('.current-score');
        currentScore.querySelector('h3').textContent = t.current;
        currentScore.querySelectorAll('.score-item span:first-child').forEach((span, index) => {
            const labels = [t.accuracy, t.completeness, t.relevance, t.clarity, t.total];
            span.textContent = `${labels[index]}:`;
        });
        
        this.content.querySelector('.score-history h3').textContent = t.history;
    }
    
    updateTheme(theme) {
        this.options.theme = theme;
        const themeStyles = this.themes[theme];
        
        this.content.style.backgroundColor = themeStyles.background;
        this.content.style.borderColor = themeStyles.border;
        
        this.content.querySelectorAll('h2, h3, span').forEach(el => {
            el.style.color = themeStyles.text;
        });
        
        this.closeBtn.style.borderColor = themeStyles.border;
        this.closeBtn.style.color = themeStyles.text;
        
        this.content.querySelectorAll('.history-item').forEach(item => {
            item.style.borderBottomColor = themeStyles.border;
            item.style.color = themeStyles.text;
        });
    }
} 