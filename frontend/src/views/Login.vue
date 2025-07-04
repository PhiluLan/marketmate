<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/AuthService.js'

const router   = useRouter()
const email    = ref('')
const password = ref('')
const error    = ref(null)

const doLogin = async () => {
  error.value = null
  try {
    await login(email.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = 'Login fehlgeschlagen'
  }
}
</script>

<template>
  <div class="p-4 max-w-sm mx-auto">
    <h1 class="text-2xl mb-4">Login</h1>
    <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>
    <input v-model="email"    type="email"    placeholder="Email"    class="w-full mb-2 border px-2 py-1 rounded"/>
    <input v-model="password" type="password" placeholder="Passwort" class="w-full mb-4 border px-2 py-1 rounded"/>
    <button @click="doLogin" class="w-full bg-blue-600 text-white py-2 rounded">
      Anmelden
    </button>
  </div>
</template>

<style scoped src="@/assets/Login.css"></style>

