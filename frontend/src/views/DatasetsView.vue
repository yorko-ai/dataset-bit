<template>
  <div class="datasets">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h2>数据集管理</h2>
              <el-button type="primary" @click="exportAllDatasets">
                导出所有数据集
              </el-button>
            </div>
          </template>

          <el-table :data="datasetList" style="width: 100%">
            <el-table-column prop="filename" label="文件名" />
            <el-table-column prop="segment_count" label="文本段落数" width="120" />
            <el-table-column prop="qa_count" label="问答对数量" width="120" />
            <el-table-column prop="avg_quality" label="平均质量" width="120">
              <template #default="{ row }">
                {{ formatQuality(row.avg_quality) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="250">
              <template #default="{ row }">
                <el-button
                  size="small"
                  type="primary"
                  @click="viewDetails(row)"
                >
                  查看详情
                </el-button>
                <el-button
                  size="small"
                  type="success"
                  @click="exportDataset(row)"
                >
                  导出
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="deleteDataset(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailsDialogVisible"
      title="数据集详情"
      width="800px"
    >
      <el-tabs v-model="activeTab">
        <el-tab-pane label="文本段落" name="segments">
          <el-table :data="currentSegments" style="width: 100%">
            <el-table-column prop="content" label="内容">
              <template #default="{ row }">
                <div class="segment-content">{{ row.content }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="qa_count" label="问答对数量" width="120" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="问答对" name="qa">
          <el-table :data="currentQAPairs" style="width: 100%">
            <el-table-column prop="question" label="问题" />
            <el-table-column prop="answer" label="答案">
              <template #default="{ row }">
                <div class="answer-content">{{ row.answer }}</div>
              </template>
            </el-table-column>
            <el-table-column prop="quality" label="质量" width="120">
              <template #default="{ row }">
                {{ formatQuality(row.quality) }}
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <!-- 导出对话框 -->
    <el-dialog
      v-model="exportDialogVisible"
      title="导出数据集"
      width="400px"
    >
      <el-form :model="exportForm" label-width="100px">
        <el-form-item label="导出格式">
          <el-select v-model="exportForm.format">
            <el-option label="Alpaca" value="alpaca" />
            <el-option label="ShareGPT" value="sharegpt" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="exportDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitExport">
            确认导出
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

interface Dataset {
  id: number
  filename: string
  segment_count: number
  qa_count: number
  avg_quality: number
  created_at: string
}

interface Segment {
  id: number
  content: string
  qa_count: number
}

interface QAPair {
  id: number
  question: string
  answer: string
  quality: number
}

const datasetList = ref<Dataset[]>([])
const detailsDialogVisible = ref(false)
const exportDialogVisible = ref(false)
const activeTab = ref('segments')
const currentSegments = ref<Segment[]>([])
const currentQAPairs = ref<QAPair[]>([])
const currentDataset = ref<Dataset | null>(null)

const exportForm = ref({
  format: 'alpaca'
})

// 获取数据集列表
const fetchDatasetList = async () => {
  try {
    const response = await axios.get('/api/stats')
    datasetList.value = response.data.data
  } catch (error) {
    ElMessage.error('获取数据集列表失败')
  }
}

// 格式化质量分数
const formatQuality = (quality: number) => {
  return (quality * 100).toFixed(1) + '%'
}

// 查看详情
const viewDetails = async (dataset: Dataset) => {
  currentDataset.value = dataset
  detailsDialogVisible.value = true
  
  try {
    const response = await axios.get(`/api/files/${dataset.id}/segments`)
    currentSegments.value = response.data.data
  } catch (error) {
    ElMessage.error('获取文本段落失败')
  }
}

// 导出数据集
const exportDataset = (dataset: Dataset) => {
  currentDataset.value = dataset
  exportDialogVisible.value = true
}

// 提交导出
const submitExport = async () => {
  if (!currentDataset.value) return
  
  try {
    const response = await axios.post(
      `/api/export/${currentDataset.value.id}`,
      exportForm.value,
      { responseType: 'blob' }
    )
    
    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${currentDataset.value.filename}_${exportForm.value.format}.json`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    exportDialogVisible.value = false
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 导出所有数据集
const exportAllDatasets = () => {
  exportForm.value.format = 'alpaca'
  exportDialogVisible.value = true
}

// 删除数据集
const deleteDataset = async (dataset: Dataset) => {
  try {
    await axios.delete(`/api/files/${dataset.id}`)
    ElMessage.success('删除成功')
    fetchDatasetList()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

// 监听标签页切换
const handleTabChange = async (tab: string) => {
  if (!currentDataset.value) return
  
  if (tab === 'qa') {
    try {
      const response = await axios.get(`/api/files/${currentDataset.value.id}/qa`)
      currentQAPairs.value = response.data.data
    } catch (error) {
      ElMessage.error('获取问答对失败')
    }
  }
}

onMounted(() => {
  fetchDatasetList()
})
</script>

<style scoped>
.datasets {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.segment-content,
.answer-content {
  max-height: 100px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 