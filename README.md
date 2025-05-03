# Dataset-Bit

Dataset-Bit是一个用于生成大型语言模型（LLM）微调数据集的工具。它可以帮助你从各种文档中提取文本，生成高质量的问答对，并导出为标准的训练数据集格式。

## 功能特点

- 支持多种文档格式（TXT、MD、DOCX、PDF）
- 智能文本分割（按段落或标题）
- 自动生成多样化的问题和答案
- 问答对质量评估
- 支持多种数据集格式（Alpaca、ShareGPT）
- 完整的文件管理和数据统计

## 技术栈

- 后端：Python + FastAPI
- 数据库：SQLite
- 前端：Vue.js
- LLM：OpenAI GPT-3.5

## 安装说明

1. 克隆项目：
```bash
git clone https://github.com/yourusername/dataset-bit.git
cd dataset-bit
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑.env文件，设置必要的配置项
```

## 使用说明

1. 启动后端服务：
```bash
python -m app.main
```

2. 启动前端开发服务器：
```bash
cd frontend
npm install
npm run dev
```

3. 访问应用：
- 后端API文档：http://localhost:8000/docs
- 前端界面：http://localhost:5173

## API接口

### 文件管理
- `POST /api/upload`：上传文件
- `GET /api/files`：获取文件列表
- `GET /api/files/{file_id}`：获取文件详情
- `DELETE /api/files/{file_id}`：删除文件

### 文本处理
- `POST /api/process/{file_id}`：处理文件并生成问答对
  - 参数：
    - `method`：分割方法（paragraph/heading）
    - `min_length`：最小段落长度
    - `max_length`：最大段落长度
    - `question_types`：问题类型列表
    - `difficulty`：问题难度
    - `questions_per_segment`：每段问题数量
    - `answer_style`：答案风格

### 问答对管理
- `GET /api/segments/{segment_id}/qa`：获取问答对

### 统计和导出
- `GET /api/stats`：获取数据集统计信息
- `POST /api/export/{file_id}`：导出数据集
  - 参数：
    - `format`：导出格式（alpaca/sharegpt）

## 项目结构

```
dataset-bit/
├── app/
│   ├── main.py              # 主应用程序
│   ├── routers/             # API路由
│   │   └── api.py
│   └── services/            # 业务服务
│       ├── file_service.py  # 文件处理服务
│       ├── llm_service.py   # LLM服务
│       └── db_service.py    # 数据库服务
├── frontend/                # 前端代码
├── uploads/                 # 上传文件目录
├── exports/                 # 导出文件目录
├── .env.example            # 环境变量示例
├── requirements.txt        # Python依赖
└── README.md              # 项目说明
```

## 开发指南

### 后端开发
1. 遵循PEP 8编码规范
2. 使用类型注解
3. 编写单元测试
4. 使用日志记录关键操作

### 前端开发
1. 使用Vue 3组合式API
2. 遵循组件化开发
3. 使用TypeScript
4. 实现响应式设计

## 贡献指南

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- GitHub：https://github.com/yourusername 