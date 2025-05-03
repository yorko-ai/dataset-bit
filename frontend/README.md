# Dataset-Bit Frontend

这是 Dataset-Bit 项目的前端部分，使用 Vue 3 + TypeScript + Element Plus 构建。

## 功能特点

- 现代化的用户界面
- 响应式设计
- 文件上传和管理
- 数据集处理和导出
- 实时状态更新

## 技术栈

- Vue 3
- TypeScript
- Element Plus
- Vue Router
- Pinia
- Axios
- Vite

## 开发环境要求

- Node.js >= 16
- npm >= 7

## 安装

1. 克隆项目
```bash
git clone https://github.com/yourusername/dataset-bit.git
cd dataset-bit/frontend
```

2. 安装依赖
```bash
npm install
```

3. 配置环境变量
```bash
cp .env.example .env
```
然后根据需要修改 `.env` 文件中的配置。

## 开发

启动开发服务器：
```bash
npm run dev
```

## 构建

构建生产版本：
```bash
npm run build
```

## 预览

预览生产构建：
```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── assets/        # 静态资源
│   ├── components/    # 公共组件
│   ├── router/        # 路由配置
│   ├── stores/        # Pinia 状态管理
│   ├── views/         # 页面组件
│   ├── App.vue        # 根组件
│   └── main.ts        # 入口文件
├── public/            # 公共资源
├── index.html         # HTML 模板
├── package.json       # 项目配置
├── tsconfig.json      # TypeScript 配置
└── vite.config.ts     # Vite 配置
```

## 主要功能

1. 文件上传
   - 支持拖拽上传
   - 支持多种文件格式
   - 文件大小限制
   - 上传进度显示

2. 文件处理
   - 文本分割
   - 问答对生成
   - 质量评估
   - 处理状态显示

3. 数据集管理
   - 数据集列表
   - 详情查看
   - 导出功能
   - 删除操作

## 开发指南

1. 组件开发
   - 使用 TypeScript 编写组件
   - 遵循 Vue 3 组合式 API 风格
   - 使用 Element Plus 组件库
   - 保持代码简洁和可维护性

2. 状态管理
   - 使用 Pinia 进行状态管理
   - 按功能模块划分 store
   - 保持状态的可预测性

3. 路由管理
   - 使用 Vue Router 进行路由管理
   - 实现路由懒加载
   - 添加路由守卫

4. API 调用
   - 使用 Axios 进行 HTTP 请求
   - 统一错误处理
   - 请求拦截和响应拦截

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 作者

Your Name

## 联系方式

- Email: your.email@example.com
- GitHub: https://github.com/yourusername 