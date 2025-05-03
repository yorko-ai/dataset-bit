<template>
  <el-container class="app-container">
    <el-header>
      <nav class="nav-header">
        <router-link to="/" class="logo">Dataset-Bit</router-link>
        <div class="nav-links">
          <router-link to="/">首页</router-link>
          <router-link to="/upload">上传文件</router-link>
          <router-link to="/datasets">数据集</router-link>
        </div>
      </nav>
    </el-header>

    <el-main>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer>
      <p>Dataset-Bit &copy; 2024</p>
    </el-footer>
  </el-container>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #409EFF;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: #606266;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #409EFF;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
}

.el-footer {
  text-align: center;
  padding: 20px;
  background-color: #fff;
  color: #909399;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 