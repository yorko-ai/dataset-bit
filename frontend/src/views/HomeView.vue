<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <template #header>
            <div class="card-header">
              <h2>欢迎使用 Dataset-Bit</h2>
            </div>
          </template>
          <p class="description">
            一个强大的LLM微调数据集自动生成工具，通过智能分割、问答生成和质量评估，快速创建高质量的训练数据集。
          </p>
          <el-button type="primary" @click="$router.push('/upload')">
            开始使用
          </el-button>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="feature-cards">
      <el-col :xs="24" :sm="12" :md="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>文档处理</h3>
            </div>
          </template>
          <ul class="feature-list">
            <li>✓ 支持 TXT、MD、DOCX、PDF</li>
            <li>✓ 智能段落分割</li>
            <li>✓ 标题识别</li>
          </ul>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>问答生成</h3>
            </div>
          </template>
          <ul class="feature-list">
            <li>✓ 事实性问题</li>
            <li>✓ 分析性问题</li>
            <li>✓ 推理性问题</li>
          </ul>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>数据导出</h3>
            </div>
          </template>
          <ul class="feature-list">
            <li>✓ Alpaca格式</li>
            <li>✓ ShareGPT格式</li>
            <li>✓ 自定义格式</li>
          </ul>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="workflow-section">
      <el-col :span="24">
        <h2>使用流程</h2>
        <el-steps :active="1" finish-status="success" align-center>
          <el-step title="上传文档" description="上传需要处理的文档，支持多种格式" />
          <el-step title="文本分割" description="选择分割方式，将文档分割成合适的片段" />
          <el-step title="生成问答" description="为每个文本片段生成问答对" />
          <el-step title="导出数据" description="选择导出格式，下载训练数据集" />
        </el-steps>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-card {
  margin-bottom: 30px;
  text-align: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.description {
  font-size: 1.1rem;
  color: #606266;
  margin: 20px 0;
}

.feature-cards {
  margin-bottom: 40px;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  margin: 10px 0;
  color: #606266;
}

.workflow-section {
  margin-top: 40px;
  text-align: center;
}

.workflow-section h2 {
  margin-bottom: 30px;
  color: #303133;
}
</style> 