<template>
  <div class="persona-container">
    <h1>🧬 Persona & Journey Builder</h1>

    <div class="persona-list">
      <div v-for="persona in personas" :key="persona._id" class="persona-card">
        <h2>{{ persona.name }}</h2>
        <p>{{ persona.description }}</p>

        <ul>
          <li><strong>Ziele:</strong> {{ persona.goals.join(', ') }}</li>
          <li><strong>Schmerzen:</strong> {{ persona.pains.join(', ') }}</li>
        </ul>

        <div v-if="persona.touchpoints.length">
          <h4>🎯 Journey:</h4>
          <ul>
            <li v-for="(tp, i) in persona.touchpoints" :key="i">
              {{ tp.stage }} – {{ tp.content }}
            </li>
          </ul>
        </div>

        <button @click="editPersona(persona)">Bearbeiten</button>
        <button @click="deletePersona(persona._id)">Löschen</button>
      </div>
    </div>

    <hr />

    <h3>{{ isEditing ? '✏️ Persona bearbeiten' : '➕ Neue Persona' }}</h3>

    <form @submit.prevent="submitPersona">
      <input v-model="form.name" placeholder="Name" required />
      <textarea v-model="form.description" placeholder="Beschreibung"></textarea>
      <input v-model="form.goalsInput" placeholder="Ziele (mit Komma trennen)" />
      <input v-model="form.painsInput" placeholder="Schmerzen (mit Komma trennen)" />

      <div class="touchpoint-input">
        <h4>Touchpoints</h4>
        <div v-for="(tp, i) in form.touchpoints" :key="i" class="touchpoint-row">
          <input v-model="tp.stage" placeholder="Phase (z. B. Awareness)" />
          <input v-model="tp.content" placeholder="Content" />
        </div>
        <button type="button" @click="form.touchpoints.push({ stage: '', content: '' })">
          ➕ Touchpoint hinzufügen
        </button>
      </div>

      <button type="submit">💾 Speichern</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import expressApi from '@/api/expressApi.js'

const personas = ref([])
const isEditing = ref(false)
const editingId = ref(null)

const form = ref({
  name: '',
  description: '',
  goalsInput: '',
  painsInput: '',
  touchpoints: []
})

async function loadPersonas() {
  const res = await expressApi.get('/personas')
  personas.value = res.data
}

function editPersona(p) {
  form.value = {
    name: p.name,
    description: p.description,
    goalsInput: p.goals.join(', '),
    painsInput: p.pains.join(', '),
    touchpoints: [...p.touchpoints]
  }
  editingId.value = p._id
  isEditing.value = true
}

async function deletePersona(id) {
  await expressApi.delete(`/personas/${id}`)
  await loadPersonas()
}

async function submitPersona() {
  const payload = {
    name: form.value.name,
    description: form.value.description,
    goals: form.value.goalsInput.split(',').map(g => g.trim()),
    pains: form.value.painsInput.split(',').map(p => p.trim()),
    touchpoints: form.value.touchpoints
  }

  if (isEditing.value) {
    await expressApi.put(`/personas/${editingId.value}`, payload)
  } else {
    await expressApi.post('/personas', payload)
  }

  form.value = {
    name: '',
    description: '',
    goalsInput: '',
    painsInput: '',
    touchpoints: []
  }

  isEditing.value = false
  editingId.value = null

  await loadPersonas()
}

onMounted(loadPersonas)
</script>

<style src="@/assets/persona.css"></style>
