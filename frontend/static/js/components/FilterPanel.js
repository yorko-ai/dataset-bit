class FilterPanel {
    constructor(container, options = {}) {
        this.container = container;
        this.lang = options.lang || 'zh';
        this.theme = options.theme || 'light';
        this.translations = this.getTranslations();
        this.themeConfig = this.getThemeConfig();
        this.onFilterChange = options.onFilterChange || (() => {});
        this.onSaveFilter = options.onSaveFilter || (() => {});
        this.onLoadFilter = options.onLoadFilter || (() => {});
        this.onDeleteFilter = options.onDeleteFilter || (() => {});
        
        this.init();
    }
    
    getTranslations() {
        return {
            zh: {
                title: '筛选条件',
                save: '保存筛选条件',
                load: '加载筛选条件',
                delete: '删除筛选条件',
                filterName: '筛选条件名称',
                keyword: '关键词',
                dateRange: '日期范围',
                startDate: '开始日期',
                endDate: '结束日期',
                scoreRange: '分数范围',
                minScore: '最小分数',
                maxScore: '最大分数',
                totalScore: '总分',
                accuracyScore: '准确性',
                completenessScore: '完整性',
                relevanceScore: '相关性',
                clarityScore: '清晰度',
                apply: '应用',
                reset: '重置',
                saveSuccess: '保存成功',
                saveFailed: '保存失败',
                deleteSuccess: '删除成功',
                deleteFailed: '删除失败',
                loadSuccess: '加载成功',
                loadFailed: '加载失败',
                confirmDelete: '确定要删除这个筛选条件吗？'
            },
            en: {
                title: 'Filter',
                save: 'Save Filter',
                load: 'Load Filter',
                delete: 'Delete Filter',
                filterName: 'Filter Name',
                keyword: 'Keyword',
                dateRange: 'Date Range',
                startDate: 'Start Date',
                endDate: 'End Date',
                scoreRange: 'Score Range',
                minScore: 'Min Score',
                maxScore: 'Max Score',
                totalScore: 'Total Score',
                accuracyScore: 'Accuracy',
                completenessScore: 'Completeness',
                relevanceScore: 'Relevance',
                clarityScore: 'Clarity',
                apply: 'Apply',
                reset: 'Reset',
                saveSuccess: 'Saved successfully',
                saveFailed: 'Failed to save',
                deleteSuccess: 'Deleted successfully',
                deleteFailed: 'Failed to delete',
                loadSuccess: 'Loaded successfully',
                loadFailed: 'Failed to load',
                confirmDelete: 'Are you sure you want to delete this filter?'
            }
        }[this.lang];
    }
    
    getThemeConfig() {
        return {
            light: {
                backgroundColor: '#ffffff',
                textColor: '#333333',
                borderColor: '#dddddd',
                inputBackgroundColor: '#ffffff',
                inputTextColor: '#333333',
                buttonBackgroundColor: '#4a90e2',
                buttonTextColor: '#ffffff',
                buttonHoverBackgroundColor: '#357abd'
            },
            dark: {
                backgroundColor: '#2d2d2d',
                textColor: '#ffffff',
                borderColor: '#3d3d3d',
                inputBackgroundColor: '#3d3d3d',
                inputTextColor: '#ffffff',
                buttonBackgroundColor: '#4a90e2',
                buttonTextColor: '#ffffff',
                buttonHoverBackgroundColor: '#357abd'
            }
        }[this.theme];
    }
    
    init() {
        this.container.innerHTML = `
            <div class="filter-panel">
                <h2>${this.translations.title}</h2>
                <div class="filter-form">
                    <div class="form-group">
                        <label>${this.translations.keyword}</label>
                        <input type="text" class="form-control" id="keyword">
                    </div>
                    <div class="form-group">
                        <label>${this.translations.dateRange}</label>
                        <div class="date-range">
                            <input type="date" class="form-control" id="startDate">
                            <span>至</span>
                            <input type="date" class="form-control" id="endDate">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>${this.translations.totalScore}</label>
                        <div class="score-range">
                            <input type="number" class="form-control" id="minTotalScore" min="0" max="100" step="0.1">
                            <span>至</span>
                            <input type="number" class="form-control" id="maxTotalScore" min="0" max="100" step="0.1">
                        </div>
                    </div>
                    <div class="form-group">
                        <label>${this.translations.accuracyScore}</label>
                        <input type="number" class="form-control" id="minAccuracyScore" min="0" max="100" step="0.1">
                    </div>
                    <div class="form-group">
                        <label>${this.translations.completenessScore}</label>
                        <input type="number" class="form-control" id="minCompletenessScore" min="0" max="100" step="0.1">
                    </div>
                    <div class="form-group">
                        <label>${this.translations.relevanceScore}</label>
                        <input type="number" class="form-control" id="minRelevanceScore" min="0" max="100" step="0.1">
                    </div>
                    <div class="form-group">
                        <label>${this.translations.clarityScore}</label>
                        <input type="number" class="form-control" id="minClarityScore" min="0" max="100" step="0.1">
                    </div>
                    <div class="form-actions">
                        <button class="btn btn-primary" id="applyFilter">${this.translations.apply}</button>
                        <button class="btn" id="resetFilter">${this.translations.reset}</button>
                        <button class="btn" id="saveFilter">${this.translations.save}</button>
                        <button class="btn" id="loadFilter">${this.translations.load}</button>
                    </div>
                </div>
            </div>
        `;
        
        this.applyStyles();
        this.bindEvents();
    }
    
    applyStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .filter-panel {
                background-color: ${this.themeConfig.backgroundColor};
                border: 1px solid ${this.themeConfig.borderColor};
                border-radius: 4px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .filter-panel h2 {
                color: ${this.themeConfig.textColor};
                margin-bottom: 20px;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-group label {
                display: block;
                color: ${this.themeConfig.textColor};
                margin-bottom: 5px;
            }
            
            .form-control {
                width: 100%;
                padding: 8px;
                border: 1px solid ${this.themeConfig.borderColor};
                border-radius: 4px;
                background-color: ${this.themeConfig.inputBackgroundColor};
                color: ${this.themeConfig.inputTextColor};
            }
            
            .date-range, .score-range {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .date-range input, .score-range input {
                flex: 1;
            }
            
            .form-actions {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            
            .btn {
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                background-color: ${this.themeConfig.buttonBackgroundColor};
                color: ${this.themeConfig.buttonTextColor};
            }
            
            .btn:hover {
                background-color: ${this.themeConfig.buttonHoverBackgroundColor};
            }
            
            .btn-primary {
                background-color: ${this.themeConfig.buttonBackgroundColor};
            }
        `;
        document.head.appendChild(style);
    }
    
    bindEvents() {
        // 应用筛选
        document.getElementById('applyFilter').addEventListener('click', () => {
            const conditions = this.getFilterConditions();
            this.onFilterChange(conditions);
        });
        
        // 重置筛选
        document.getElementById('resetFilter').addEventListener('click', () => {
            this.resetForm();
            this.onFilterChange({});
        });
        
        // 保存筛选
        document.getElementById('saveFilter').addEventListener('click', () => {
            const name = prompt(this.translations.filterName);
            if (name) {
                const conditions = this.getFilterConditions();
                this.onSaveFilter(name, conditions);
            }
        });
        
        // 加载筛选
        document.getElementById('loadFilter').addEventListener('click', () => {
            this.loadSavedFilters();
        });
    }
    
    getFilterConditions() {
        return {
            keyword: document.getElementById('keyword').value,
            start_date: document.getElementById('startDate').value,
            end_date: document.getElementById('endDate').value,
            min_total_score: document.getElementById('minTotalScore').value || null,
            max_total_score: document.getElementById('maxTotalScore').value || null,
            min_accuracy_score: document.getElementById('minAccuracyScore').value || null,
            min_completeness_score: document.getElementById('minCompletenessScore').value || null,
            min_relevance_score: document.getElementById('minRelevanceScore').value || null,
            min_clarity_score: document.getElementById('minClarityScore').value || null
        };
    }
    
    resetForm() {
        document.getElementById('keyword').value = '';
        document.getElementById('startDate').value = '';
        document.getElementById('endDate').value = '';
        document.getElementById('minTotalScore').value = '';
        document.getElementById('maxTotalScore').value = '';
        document.getElementById('minAccuracyScore').value = '';
        document.getElementById('minCompletenessScore').value = '';
        document.getElementById('minRelevanceScore').value = '';
        document.getElementById('minClarityScore').value = '';
    }
    
    async loadSavedFilters() {
        try {
            const response = await fetch('/api/filters');
            const data = await response.json();
            
            if (data.success) {
                const filters = data.data;
                if (filters.length === 0) {
                    alert(this.translations.noFilters);
                    return;
                }
                
                const filterNames = filters.map(f => f.name);
                const selectedName = prompt(
                    this.translations.selectFilter + '\n' + filterNames.join('\n')
                );
                
                if (selectedName) {
                    const selectedFilter = filters.find(f => f.name === selectedName);
                    if (selectedFilter) {
                        const conditions = JSON.parse(selectedFilter.filter_conditions);
                        this.setFilterConditions(conditions);
                        this.onLoadFilter(selectedFilter.id);
                    }
                }
            } else {
                alert(this.translations.loadFailed);
            }
        } catch (error) {
            console.error('加载筛选条件失败:', error);
            alert(this.translations.loadFailed);
        }
    }
    
    setFilterConditions(conditions) {
        document.getElementById('keyword').value = conditions.keyword || '';
        document.getElementById('startDate').value = conditions.start_date || '';
        document.getElementById('endDate').value = conditions.end_date || '';
        document.getElementById('minTotalScore').value = conditions.min_total_score || '';
        document.getElementById('maxTotalScore').value = conditions.max_total_score || '';
        document.getElementById('minAccuracyScore').value = conditions.min_accuracy_score || '';
        document.getElementById('minCompletenessScore').value = conditions.min_completeness_score || '';
        document.getElementById('minRelevanceScore').value = conditions.min_relevance_score || '';
        document.getElementById('minClarityScore').value = conditions.min_clarity_score || '';
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