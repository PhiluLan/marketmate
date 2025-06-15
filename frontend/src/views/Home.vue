<script setup>
import { onMounted, ref } from 'vue'
import { getMe, logout } from '@/services/AuthService'

const user = ref(null)

onMounted(async () => {
  try {
    user.value = await getMe()
  } catch {
    // nicht eingeloggt, ggf. weiterleiten
  }
})
</script>

<template>
  <div>
    <p v-if="user">Hallo {{ user.email }}</p>
    <button @click="logout()">Logout</button>
  </div>
</template>
