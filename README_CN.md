# Dataset-Bit 🚀

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-green.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.0-brightgreen.svg)](https://vuejs.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/yorkoliu/dataset-bit?style=social)](https://github.com/yorkoliu/dataset-bit/stargazers)

</div>

## 📖 项目简介

Dataset-Bit 是一个强大的开源工具，专门用于生成和优化大型语言模型（LLM）的微调数据集。它能够智能地从各种文档中提取文本，生成高质量的问答对，并导出为标准的训练数据集格式。无论是研究人员、开发者还是数据科学家，都可以使用 Dataset-Bit 来快速构建高质量的 LLM 训练数据。

### ✨ 核心特性

- 📚 **多格式支持**：支持 TXT、MD、DOCX、PDF 等多种文档格式
- 🔍 **智能分割**：基于段落或标题的智能文本分割
- 🤖 **AI 生成**：自动生成多样化、高质量的问题和答案
- 📊 **质量评估**：内置问答对质量评估系统
- 📦 **格式转换**：支持 Alpaca、ShareGPT 等多种数据集格式
- 📈 **数据统计**：完整的文件管理和数据统计分析
- 🔄 **批量处理**：支持批量文件处理和并行处理
- 🎯 **自定义配置**：灵活的参数配置和自定义选项

## 🛠️ 技术栈

### 后端
- **框架**：FastAPI
- **语言**：Python 3.8+
- **数据库**：SQLite
- **AI 模型**：OpenAI GPT-3.5
- **文档处理**：PyPDF2, python-docx, markdown

### 前端
- **框架**：Vue.js 3
- **构建工具**：Vite
- **UI 组件**：Element Plus
- **状态管理**：Pinia
- **HTTP 客户端**：Axios

## 🚀 快速开始

### 系统要求
- Python 3.8 或更高版本
- Node.js 16 或更高版本
- 至少 4GB RAM
- 稳定的网络连接

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/yorkoliu/dataset-bit.git
cd dataset-bit
```

2. **设置 Python 环境**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，设置必要的配置
# 特别是 OPENAI_API_KEY 和其他必要的 API 密钥
```

4. **启动服务**
```bash
# 启动后端服务
python -m app.main

# 新开一个终端，启动前端服务
cd frontend
npm install
npm run dev
```

5. **访问应用**
- 前端界面：http://localhost:5173
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

## 📚 详细文档

### API 接口

#### 文件管理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/upload` | POST | 上传文件 |
| `/api/files` | GET | 获取文件列表 |
| `/api/files/{file_id}` | GET | 获取文件详情 |
| `/api/files/{file_id}` | DELETE | 删除文件 |

#### 文本处理
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/process/{file_id}` | POST | 处理文件并生成问答对 |
| `/api/segments/{segment_id}/qa` | GET | 获取问答对 |

#### 数据导出
| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/export/{file_id}` | POST | 导出数据集 |
| `/api/stats` | GET | 获取数据集统计信息 |

### 配置参数

#### 文本处理参数
```json
{
  "method": "paragraph",  // 分割方法：paragraph/heading
  "min_length": 100,     // 最小段落长度
  "max_length": 1000,    // 最大段落长度
  "question_types": ["what", "how", "why"],  // 问题类型
  "difficulty": "medium",  // 问题难度
  "questions_per_segment": 3,  // 每段问题数量
  "answer_style": "detailed"  // 答案风格
}
```

## 📁 项目结构

```
dataset-bit/
├── app/
│   ├── main.py              # 主应用程序入口
│   ├── routers/             # API 路由定义
│   │   └── api.py
│   ├── services/            # 业务服务层
│   │   ├── file_service.py  # 文件处理服务
│   │   ├── llm_service.py   # LLM 服务
│   │   └── db_service.py    # 数据库服务
│   ├── models/              # 数据模型
│   │   └── database.py
│   └── utils/               # 工具函数
│       ├── batch_processor.py
│       ├── file_handler.py
│       └── quality_evaluator.py
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/      # Vue 组件
│   │   ├── views/          # 页面视图
│   │   ├── store/          # 状态管理
│   │   └── api/            # API 调用
│   └── public/             # 静态资源
├── tests/                   # 测试用例
├── uploads/                 # 上传文件目录
├── exports/                 # 导出文件目录
├── .env.example            # 环境变量示例
├── requirements.txt        # Python 依赖
└── README.md              # 项目说明
```

## 👥 开发指南

### 后端开发规范
1. 遵循 PEP 8 编码规范
2. 使用类型注解
3. 编写单元测试（覆盖率 > 80%）
4. 使用日志记录关键操作
5. 使用异步编程处理 I/O 操作

### 前端开发规范
1. 使用 Vue 3 组合式 API
2. 遵循组件化开发原则
3. 使用 TypeScript 进行类型检查
4. 实现响应式设计
5. 遵循 ESLint 规范

## 🤝 贡献指南

我们欢迎任何形式的贡献，包括但不限于：

1. 提交问题和建议
2. 改进文档
3. 提交代码改进
4. 分享使用经验

### 贡献流程

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 提交信息遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范
- 代码变更需要包含相应的测试
- 确保所有测试通过
- 更新相关文档

## 📝 更新日志

### v1.0.0 (2025-05-03)
- 🎉 首次发布
- ✨ 实现基础功能
- 📚 支持多种文档格式
- 🤖 集成 OpenAI GPT-3.5
- 🎨 实现基础 UI 界面

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 作者：刘天斯 (York Liu)
- 邮箱：liutiansi@gmail.com
- 微信：yorkoliu
- GitHub：[yorkoliu](https://github.com/yorkoliu)
- 项目主页：[Dataset-Bit](https://github.com/yorkoliu/dataset-bit)

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/yorkoliu">York Liu</a></sub>
</div> 