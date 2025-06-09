<template>
  <el-tooltip content="上传文件（支持图片/PDF）">
    <el-button 
      type="text" 
      icon="el-icon-upload" 
      circle
      @click="triggerUpload"
    />
  </el-tooltip>
  
  <input
    ref="fileInput"
    type="file"
    hidden
    accept=".jpg,.jpeg,.png,.pdf"
    @change="handleFileChange"
  >
</template>

<script setup>
const emit = defineEmits(['upload'])

const fileInput = ref(null)

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    // 验证文件类型
    const isValid = ['image/jpeg', 'image/png', 'application/pdf'].includes(file.type)
    if (!isValid) {
      ElMessage.error('仅支持 JPG/PNG/PDF 格式')
      return
    }
    emit('upload', file)
  }
}
</script>