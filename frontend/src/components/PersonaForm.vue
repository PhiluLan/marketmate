<template>
  <div class="persona-form">
    <h2>🧍 Neue Persona erstellen</h2>

    <form @submit.prevent="handleSubmit">
      <input v-model="persona.name" placeholder="Name der Persona" required />
      <input v-model="persona.ageGroup" placeholder="Alter / Altersgruppe" required />
      <input v-model="persona.role" placeholder="Rolle / Jobtitel" required />
      <input v-model="persona.industry" placeholder="Branche" required />
      <textarea v-model="persona.goals" placeholder="Ziele & Bedürfnisse" />
      <textarea v-model="persona.challenges" placeholder="Herausforderungen" />

      <button type="submit">Speichern</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PersonaService from '@/services/PersonaService'

const emit = defineEmits(['persona-created'])

const persona = ref({
  name: '',
  ageGroup: '',
  role: '',
  industry: '',
  goals: '',
  challenges: ''
})

async function handleSubmit() {
  try {
    const saved = await PersonaService.createPersona(persona.value)
    emit('persona-created', saved)
    Object.keys(persona.value).forEach(k => persona.value[k] = '')
  } catch (err) {
    console.error('Fehler beim Speichern der Persona:', err)
  }
}
</script>

<style src="@/assets/persona.css" />
