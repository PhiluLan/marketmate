<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/services/AuthService.js'

const router = useRouter()
const form = reactive({
  email: '',
  password: '',
  role: 'KMU',
  first_name: '',
  last_name: '',
  website_url: '',
  company_name: '',
  industry: '',
  instagram_url: '',
  facebook_url: '',
  linkedin_url: '',
})
const error = ref(null)

const registerUser = async () => {
  error.value = null
  try {
    // Wir übergeben das gesamte form-Objekt
    await register(form)
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
        <label class="block mb-1">E-Mail</label>
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
      <div>
        <label class="block mb-1">Vorname</label>
        <input v-model="form.first_name" type="text" required class="w-full border px-2 py-1 rounded" />
      </div>
      <div>
        <label class="block mb-1">Nachname</label>
        <input v-model="form.last_name" type="text" required class="w-full border px-2 py-1 rounded" />
      </div>
      <div>
        <label>Webseite</label>
        <input v-model="form.website_url" type="url" />
      </div>
      <div>
        <label>Firmenname</label>
        <input v-model="form.company_name" type="text" />
      </div>
      <div>
        <label>Branche</label>
        <input v-model="form.industry" type="text" />
      </div>
      <div>
        <label>Instagram (optional)</label>
        <input v-model="form.instagram_url" type="url" />
      </div>
      <div>
        <label>Facebook (optional)</label>
        <input v-model="form.facebook_url" type="url" />
      </div>
      <div>
        <label>LinkedIn (optional)</label>
        <input v-model="form.linkedin_url" type="url" />
      </div>

      <button type="submit" class="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
        Registrieren
      </button>
    </form>
    <p v-if="error" class="text-red-600 mt-2">{{ error }}</p>
  </div>
</template>

<style scoped src="@/assets/Register.css"></style>
