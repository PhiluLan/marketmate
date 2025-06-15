<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/AuthService.js'   // Hole die named-function

const router = useRouter()
const form = reactive({ email: '', password: '', role: 'KMU' })
const error = ref(null)

const registerUser = async () => {
  error.value = null
  try {
    await register(form.email, form.password, form.role)
    router.push('/login')
  } catch (e) {
    error.value = e.response?.data || 'Registrierung fehlgeschlagen'
  }
}
</script>

<template>
  <div class="p-4 max-w-md mx-auto">
    <h1 class="text-2xl mb-4">Registrieren</h1>
    <form @submit.prevent="registerUser" class="space-y-4">
      <div>
        <label class="block mb-1">Email</label>
        <input v-model="form.email" type="email" required class="w-full border px-2 py-1 rounded" />
      </div>
      <div>
        <label class="block mb-1">Passwort</label>
        <input v-model="form.password" type="password" required class="w-full border px-2 py-1 rounded" />
      </div>
      <div>
        <label class="block mb-1">Rolle</label>
        <select v-model="form.role" required class="w-full border px-2 py-1 rounded">
          <option value="KMU">KMU</option>
          <option value="Agentur">Agentur</option>
        </select>
      </div>
      <button type="submit" class="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
        Registrieren
      </button>
    </form>
    <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
  </div>
</template>
