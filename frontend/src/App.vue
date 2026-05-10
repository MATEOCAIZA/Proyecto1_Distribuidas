<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()

onMounted(() => {
  chatStore.initializeSocket()
})
</script>

<style scoped>
#app {
  min-height: 100vh;
}
</style>