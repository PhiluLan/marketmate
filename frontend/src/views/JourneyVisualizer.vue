<template>
  <div class="journey-wrapper">
    <h1>🧭 Customer Journey Visualisierung</h1>

    <div v-for="persona in personas" :key="persona._id" class="journey-lane">
      <h2>👤 {{ persona.name }}</h2>
      <div class="journey-columns">
        <div
          v-for="phase in phases"
          :key="phase"
          class="journey-column"
        >
          <h3>{{ phase }}</h3>

          <div
            v-for="(tp, i) in getTouchpoints(persona, phase)"
            :key="i"
            class="touchpoint-card"
          >
            {{ tp.content }}
            <div class="touchpoint-actions">
              <button @click="editTouchpoint(persona, phase, i)">✏️</button>
              <button @click="deleteTouchpoint(persona, phase, i)">🗑️</button>
            </div>
          </div>

          <button class="add-btn" @click="openModal(persona, phase)">➕ Touchpoint</button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h3>{{ isEditingTouchpoint ? '✏️ Touchpoint bearbeiten' : '➕ Touchpoint hinzufügen' }}</h3>
      <p><strong>{{ selectedPhase }}</strong> – {{ selectedPersona?.name }}</p>
      <input v-model="newContent" placeholder="z. B. Artikel zu SEO-Basics" />
      <div class="actions">
        <button @click="addTouchpoint">💾 Speichern</button>
        <button @click="showModal = false">Abbrechen</button>
        <button @click="generateSuggestion" type="button">🪄 Vorschlag generieren</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import expressApi from '@/api/expressApi.js'
import ChatService from '@/services/ChatService.js'

const showModal = ref(false)
const selectedPersona = ref(null)
const selectedPhase = ref('')
const newContent = ref('')
const isEditingTouchpoint = ref(false)
const editingIndex = ref(null)

const personas = ref([])
const phases = ['Awareness', 'Consideration', 'Decision', 'Retention', 'Advocacy']

async function loadPersonas() {
  const res = await expressApi.get('/personas')
  personas.value = res.data
}

function getTouchpoints(persona, phase) {
  return persona.touchpoints?.filter(tp => tp.stage === phase) || []
}

function openModal(persona, phase) {
  selectedPersona.value = persona
  selectedPhase.value = phase
  newContent.value = ''
  showModal.value = true
  isEditingTouchpoint.value = false
  editingIndex.value = null
}

async function addTouchpoint() {
  if (!newContent.value.trim()) return

  const existing = selectedPersona.value.touchpoints.filter(tp => tp.stage !== selectedPhase.value)
  const phaseTouchpoints = getTouchpoints(selectedPersona.value, selectedPhase.value)

  if (isEditingTouchpoint.value && editingIndex.value !== null) {
    phaseTouchpoints[editingIndex.value].content = newContent.value.trim()
  } else {
    phaseTouchpoints.push({ stage: selectedPhase.value, content: newContent.value.trim() })
  }

  const updated = {
    ...selectedPersona.value,
    touchpoints: [...existing, ...phaseTouchpoints]
  }

  await expressApi.put(`/personas/${selectedPersona.value._id}`, updated)

  showModal.value = false
  isEditingTouchpoint.value = false
  editingIndex.value = null
  await loadPersonas()
}

function editTouchpoint(persona, phase, index) {
  selectedPersona.value = persona
  selectedPhase.value = phase
  editingIndex.value = index
  newContent.value = persona.touchpoints.filter(tp => tp.stage === phase)[index].content
  isEditingTouchpoint.value = true
  showModal.value = true
}

function deleteTouchpoint(persona, phase, index) {
  const updatedTouchpoints = persona.touchpoints.filter((tp, i) =>
    !(tp.stage === phase && getTouchpoints(persona, phase).indexOf(tp) === index)
  )

  expressApi.put(`/personas/${persona._id}`, {
    ...persona,
    touchpoints: updatedTouchpoints
  }).then(loadPersonas)
}

async function generateSuggestion() {
  const prompt = `Gib mir einen prägnanten, praktischen Content-Touchpoint für die Phase "${selectedPhase.value}" einer Customer Journey für folgende Persona:\n
Name: ${selectedPersona.value.name}
Beschreibung: ${selectedPersona.value.description}
Ziele: ${selectedPersona.value.goals.join(', ')}
Schmerzen: ${selectedPersona.value.pains.join(', ')}

Format: 1 knackiger Satz, max. 120 Zeichen.`

  newContent.value = await ChatService.sendMessage(prompt)
}

onMounted(loadPersonas)
</script>

<style scoped>
.journey-wrapper {
  padding: 20px;
}

.journey-lane {
  margin-bottom: 40px;
  background: #f9f9f9;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 0 4px rgba(0,0,0,0.08);
}

.journey-columns {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 12px;
}

.journey-column {
  flex: 0 0 220px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 12px;
  min-height: 200px;
}

.journey-column h3 {
  margin-top: 0;
  font-size: 16px;
  border-bottom: 1px solid #eee;
  padding-bottom: 6px;
}

.touchpoint-card {
  background: #e0f2fe;
  border: 1px solid #90cdf4;
  padding: 8px;
  border-radius: 4px;
  margin-bottom: 8px;
  font-size: 14px;
}

.add-btn {
  background: transparent;
  color: #2563eb;
  border: none;
  cursor: pointer;
  font-size: 14px;
  margin-top: 4px;
}

.touchpoint-actions {
  display: flex;
  gap: 4px;
  margin-top: 4px;
}

.touchpoint-actions button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 320px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.modal input {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.actions {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
</style>
