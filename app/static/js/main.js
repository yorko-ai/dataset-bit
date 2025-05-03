// 全局工具函数
const utils = {
    // 格式化文件大小
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // 格式化日期时间
    formatDateTime(date) {
        return new Date(date).toLocaleString();
    },

    // 显示提示消息
    showMessage(message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
        setTimeout(() => alertDiv.remove(), 5000);
    },

    // 显示加载动画
    showLoading(element) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading';
        element.appendChild(loadingDiv);
        return loadingDiv;
    },

    // 隐藏加载动画
    hideLoading(loadingElement) {
        if (loadingElement) {
            loadingElement.remove();
        }
    },

    // 防抖函数
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 节流函数
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// API请求函数
const api = {
    // 通用请求函数
    async request(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || '请求失败');
            }
            return data;
        } catch (error) {
            utils.showMessage(error.message, 'danger');
            throw error;
        }
    },

    // 上传文件
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        return this.request('/api/upload', {
            method: 'POST',
            body: formData,
            headers: {} // 不设置Content-Type，让浏览器自动设置
        });
    },

    // 获取文件列表
    async getFiles() {
        return this.request('/api/files');
    },

    // 处理文件
    async processFile(fileId) {
        return this.request(`/api/split?file_id=${fileId}`, {
            method: 'POST'
        });
    },

    // 删除文件
    async deleteFile(fileId) {
        return this.request(`/api/files/${fileId}`, {
            method: 'DELETE'
        });
    },

    // 导出数据集
    async exportDataset(format = 'alpaca', includeMetadata = true) {
        return this.request('/api/export', {
            method: 'POST',
            body: JSON.stringify({ format, include_metadata: includeMetadata })
        });
    }
};

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化工具提示
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 添加页面过渡动画
    document.querySelectorAll('.fade-in').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 100);
    });
}); 