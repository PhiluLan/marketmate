<template>
  <div class="max-w-md mx-auto p-6 bg-white rounded shadow">
    <h1 class="text-2xl mb-4 font-bold">Website hinzufügen</h1>
    <form @submit.prevent="addWebsite" class="space-y-4">
      <div>
        <label class="block mb-1">Name</label>
        <input v-model="form.name" type="text" required class="w-full border px-2 py-1 rounded" />
      </div>
      <div>
        <label class="block mb-1">URL <span class="text-gray-500 text-sm">(mit oder ohne https://)</span></label>
        <input v-model="form.url" type="text" required class="w-full border px-2 py-1 rounded" placeholder="z.B. https://beispiel.de" />
      </div>
      <button type="submit" class="bg-green-600 text-white rounded px-4 py-2 hover:bg-green-700 w-full">
        Website speichern
      </button>
    </form>
    <div v-if="error" class="mt-2 text-red-600">{{ error }}</div>
    <div v-if="success" class="mt-2 text-green-600">Website wurde gespeichert!</div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/AuthService'

const router = useRouter()
const form = reactive({ name: '', url: '' })
const error = ref(null)
const success = ref(false)

const addWebsite = async () => {
  error.value = null
  success.value = false
  try {
    await api.post('/websites/', {
      name: form.name,
      url: form.url    // Backend erwartet dieses Feld!
    })
    success.value = true
    setTimeout(() => router.push('/'), 1200)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Fehler beim Speichern'
  }
}
</script>
