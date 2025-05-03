<template>
  <div class="upload">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h2>上传文件</h2>
            </div>
          </template>

          <el-upload
            class="upload-area"
            drag
            action="/api/upload"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
            multiple
            :limit="5"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽文件到此处或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 TXT、MD、DOCX、PDF 格式文件
              </div>
            </template>
          </el-upload>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="file-list">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <h3>已上传文件</h3>
            </div>
          </template>

          <el-table :data="fileList" style="width: 100%">
            <el-table-column prop="filename" label="文件名" />
            <el-table-column prop="filetype" label="类型" width="100" />
            <el-table-column prop="filesize" label="大小" width="120">
              <template #default="{ row }">
                {{ formatFileSize(row.filesize) }}
              </template>
            </el-table-column>
            <el-table-column prop="upload_time" label="上传时间" width="180" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button
                  size="small"
                  type="primary"
                  @click="processFile(row)"
                  :disabled="row.status !== '待处理'"
                >
                  处理
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="deleteFile(row)"
                >
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- 处理文件对话框 -->
    <el-dialog
      v-model="processDialogVisible"
      title="处理文件"
      width="500px"
    >
      <el-form :model="processForm" label-width="120px">
        <el-form-item label="分割方法">
          <el-select v-model="processForm.method">
            <el-option label="按段落" value="paragraph" />
            <el-option label="按标题" value="heading" />
          </el-select>
        </el-form-item>
        <el-form-item label="最小长度">
          <el-input-number v-model="processForm.min_length" :min="50" :max="500" />
        </el-form-item>
        <el-form-item label="最大长度">
          <el-input-number v-model="processForm.max_length" :min="500" :max="5000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="processDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitProcess">
            开始处理
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import axios from 'axios'

interface FileItem {
  id: number
  filename: string
  filetype: string
  filesize: number
  upload_time: string
  status: string
}

const fileList = ref<FileItem[]>([])
const processDialogVisible = ref(false)
const currentFile = ref<FileItem | null>(null)

const processForm = ref({
  method: 'paragraph',
  min_length: 100,
  max_length: 1000
})

// 获取文件列表
const fetchFileList = async () => {
  try {
    const response = await axios.get('/api/files')
    fileList.value = response.data.data
  } catch (error) {
    ElMessage.error('获取文件列表失败')
  }
}

// 处理上传成功
const handleUploadSuccess = (response: any) => {
  ElMessage.success('文件上传成功')
  fetchFileList()
}

// 处理上传失败
const handleUploadError = () => {
  ElMessage.error('文件上传失败')
}

// 上传前检查
const beforeUpload = (file: File) => {
  const allowedTypes = ['.txt', '.md', '.docx', '.pdf']
  const extension = '.' + file.name.split('.').pop()?.toLowerCase()
  
  if (!allowedTypes.includes(extension)) {
    ElMessage.error('不支持的文件类型')
    return false
  }
  
  return true
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 获取状态标签类型
const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    '待处理': 'warning',
    '处理中': 'primary',
    '已完成': 'success',
    '失败': 'danger'
  }
  return types[status] || 'info'
}

// 处理文件
const processFile = (file: FileItem) => {
  currentFile.value = file
  processDialogVisible.value = true
}

// 提交处理
const submitProcess = async () => {
  if (!currentFile.value) return
  
  try {
    await axios.post(`/api/process/${currentFile.value.id}`, processForm.value)
    ElMessage.success('开始处理文件')
    processDialogVisible.value = false
    fetchFileList()
  } catch (error) {
    ElMessage.error('处理文件失败')
  }
}

// 删除文件
const deleteFile = async (file: FileItem) => {
  try {
    await axios.delete(`/api/files/${file.id}`)
    ElMessage.success('文件删除成功')
    fetchFileList()
  } catch (error) {
    ElMessage.error('删除文件失败')
  }
}

onMounted(() => {
  fetchFileList()
})
</script>

<style scoped>
.upload {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.upload-area {
  width: 100%;
}

.file-list {
  margin-top: 20px;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 7px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 