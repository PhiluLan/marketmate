<template>
  <div class="journey-container">
    <h1>🚀 Customer Journey Builder</h1>

    <div class="journey-list">
      <div v-for="j in journeys" :key="j._id" class="journey-card">
        <h2>{{ j.name }} – ({{ j.persona?.name || 'Unbekannt' }})</h2>
        <p>{{ j.description }}</p>

        <ul v-if="j.touchpoints.length">
          <li v-for="(tp, i) in j.touchpoints" :key="i">
            <strong>{{ tp.stage }}</strong>: {{ tp.content }} <em>({{ tp.channel || '–' }})</em>
          </li>
        </ul>

        <button @click="editJourney(j)">Bearbeiten</button>
        <button @click="deleteJourney(j._id)">Löschen</button>
      </div>
    </div>

    <hr />

    <h3>{{ isEditing ? '✏️ Journey bearbeiten' : '➕ Neue Journey' }}</h3>

    <form @submit.prevent="submitJourney">
      <input v-model="form.name" placeholder="Name der Journey" required />
      <textarea v-model="form.description" placeholder="Beschreibung"></textarea>

      <select v-model="form.persona" required>
        <option disabled value="">– Persona wählen –</option>
        <option v-for="p in personas" :value="p._id" :key="p._id">{{ p.name }}</option>
      </select>

      <div class="touchpoint-input">
        <h4>Touchpoints</h4>
        <div v-for="(tp, i) in form.touchpoints" :key="i" class="touchpoint-row">
          <input v-model="tp.stage" placeholder="Phase (Awareness...)" />
          <input v-model="tp.content" placeholder="Inhalt / Aktion" />
          <input v-model="tp.channel" placeholder="Kanal (z. B. LinkedIn)" />
        </div>
        <button type="button" @click="form.touchpoints.push({ stage: '', content: '', channel: '' })">
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

const journeys = ref([])
const personas = ref([])
const isEditing = ref(false)
const editingId = ref(null)

const form = ref({
  name: '',
  description: '',
  persona: '',
  touchpoints: []
})

async function loadJourneys() {
  const res = await expressApi.get('/journeys')
  journeys.value = res.data
}

async function loadPersonas() {
  const res = await expressApi.get('/personas')
  personas.value = res.data
}

function editJourney(j) {
  form.value = {
    name: j.name,
    description: j.description,
    persona: j.persona?._id || '',
    touchpoints: [...j.touchpoints]
  }
  editingId.value = j._id
  isEditing.value = true
}

async function deleteJourney(id) {
  await expressApi.delete(`/journeys/${id}`)
  await loadJourneys()
}

async function submitJourney() {
  const payload = { ...form.value }

  if (isEditing.value) {
    await expressApi.put(`/journeys/${editingId.value}`, payload)
  } else {
    await expressApi.post('/journeys', payload)
  }

  // 🔁 Synchronisiere Touchpoints mit zugehöriger Persona
  const selected = personas.value.find(p => p._id === form.value.persona)
  if (selected) {
    const updatedTouchpoints = [...selected.touchpoints, ...form.value.touchpoints]
    await expressApi.put(`/personas/${selected._id}`, {
      ...selected,
      touchpoints: updatedTouchpoints
    })
  }

  // Reset Form
  form.value = {
    name: '',
    description: '',
    persona: '',
    touchpoints: []
  }

  isEditing.value = false
  editingId.value = null

  await loadJourneys()
}


onMounted(() => {
  loadPersonas()
  loadJourneys()
})
</script>

<style src="@/assets/journey.css"></style>
