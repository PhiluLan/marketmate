<template>
  <div>
    <h1 style="font-size: 24px; font-weight: bold; margin-bottom: 16px;">📆 Redaktionskalender</h1>

    <div class="calendar">
      <!-- Header -->
      <div class="header-cell"></div>
      <div v-for="day in weekdays" :key="day" class="header-cell">{{ day }}</div>

      <!-- Ganztags-Terminzelle -->
      <div class="all-day-row">
        <div class="time-cell">Ganztägig</div>
        <div v-for="day in weekdays" :key="day + '-allDay'" class="slot all-day-slot">
          <div
            v-for="(event, index) in findAllDayEvents(day)"
            :key="index"
            class="event all-day"
            @click.stop="editEvent(event)"
          >
            {{ event.title }}
          </div>
        </div>
      </div>

      <!-- Zeitraster -->
      <template v-for="(hour, i) in timeSlots" :key="i">
        <div class="time-cell">{{ hour }}</div>
        <div
          v-for="day in weekdays"
          :key="day + '-' + hour"
          class="slot"
          @dblclick="createEvent(day, i)"
        >
          <div
            v-for="(event, index) in findEvents(day, i)"
            :key="index"
            class="event"
            :style="{ height: calcEventHeight(event) + 'px' }"
            @click.stop="editEvent(event)"
          >
            {{ event.title }}
          </div>
        </div>
      </template>
    </div>

    <!-- Modal -->
    <div v-if="showModal" class="modal">
      <h3>{{ isEditing ? '🖊 Termin bearbeiten' : '🆕 Neuer Termin' }}</h3>

      <input v-model="modalEvent.title" placeholder="Titel" class="input" />
      <input v-model="modalEvent.person" placeholder="Person einladen" class="input" />

      <label class="checkbox">
        <input type="checkbox" v-model="modalEvent.allDay" />
        Ganztägig
      </label>

      <input type="date" v-model="modalEvent.date" class="input" />

      <div v-if="!modalEvent.allDay">
        <input type="time" v-model="modalEvent.startTime" step="1800" class="input" />
        <input type="time" v-model="modalEvent.endTime" step="1800" class="input" />
      </div>

      <input
        id="location-input"
        v-model="modalEvent.location"
        placeholder="Ort (Adresse)"
        class="input"
      />
      <textarea v-model="modalEvent.description" placeholder="Beschreibung" class="textarea"></textarea>

      <select v-model="modalEvent.repeat" class="input">
        <option value="none">Ohne</option>
        <option value="daily">Täglich</option>
        <option value="weekly">Wöchentlich</option>
        <option value="monthly">Monatlich</option>
        <option value="yearly">Jährlich</option>
      </select>

      <input type="file" multiple @change="handleFileUpload" class="input" />

      <select v-model="modalEvent.reminder" class="input">
        <option value="none">Keine Erinnerung</option>
        <option value="5">5 Minuten vorher</option>
        <option value="10">10 Minuten vorher</option>
        <option value="15">15 Minuten vorher</option>
        <option value="30">30 Minuten vorher</option>
        <option value="60">1 Stunde vorher</option>
        <option value="1440">1 Tag vorher</option>
        <option value="10080">1 Woche vorher</option>
      </select>

      <div class="modal-actions">
        <button @click="saveEvent" class="btn-primary">Speichern</button>
        <button @click="cancelEdit" class="btn-cancel">Abbrechen</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
let autocomplete = null

onMounted(() => {
  const waitForGoogle = setInterval(() => {
    const input = document.getElementById('location-input')
    if (input && window.google && window.google.maps && window.google.maps.places) {
      autocomplete = new window.google.maps.places.Autocomplete(input, { types: ['geocode'] })

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace()
        modalEvent.value.location = place?.formatted_address || input.value
      })

      clearInterval(waitForGoogle)
    }
  }, 500)
})


const weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
const timeSlots = Array.from({ length: 48 }, (_, i) => {
  const h = Math.floor(i / 2).toString().padStart(2, '0')
  const m = i % 2 === 0 ? '00' : '30'
  return `${h}:${m}`
})

const events = ref([])
const showModal = ref(false)
const isEditing = ref(false)
const editingIndex = ref(null)

const modalEvent = ref({
  title: '',
  person: '',
  allDay: false,
  date: '',
  startTime: '',
  endTime: '',
  location: '',
  description: '',
  repeat: 'none',
  attachments: [],
  reminder: 'none',
  day: ''
})

function waitForGoogleMaps() {
  return new Promise((resolve) => {
    const check = () => {
      if (window.google && window.google.maps && window.google.maps.places) {
        resolve()
      } else {
        setTimeout(check, 300)
      }
    }
    check()
  })
}

function handleFileUpload(e) {
  modalEvent.value.attachments = Array.from(e.target.files)
}

function createEvent(day, slotIndex) {
  const today = new Date().toISOString().split('T')[0]
  const [h, m] = timeSlots[slotIndex].split(':')
  const startTime = `${h}:${m}`
  const [eh, em] = timeSlots[slotIndex + 2] ? timeSlots[slotIndex + 2].split(':') : ['23', '59']
  const endTime = `${eh}:${em}`

  modalEvent.value = {
    title: '',
    person: '',
    allDay: false,
    date: today,
    startTime,
    endTime,
    location: '',
    description: '',
    repeat: 'none',
    attachments: [],
    reminder: 'none',
    day
  }

  showModal.value = true
  isEditing.value = false
  editingIndex.value = null
}

function editEvent(event) {
  modalEvent.value = { ...event }
  editingIndex.value = events.value.indexOf(event)
  isEditing.value = true
  showModal.value = true
}

function saveEvent() {
  const newEvent = { ...modalEvent.value }

  if (!newEvent.allDay) {
    const startIndex = timeSlots.findIndex(t => t === newEvent.startTime)
    const endIndex = timeSlots.findIndex(t => t === newEvent.endTime)
    newEvent.startIndex = startIndex
    newEvent.endIndex = endIndex
  }

  if (isEditing.value && editingIndex.value !== null) {
    events.value[editingIndex.value] = newEvent
  } else {
    events.value.push(newEvent)
  }

  showModal.value = false
  isEditing.value = false
  editingIndex.value = null
}

function cancelEdit() {
  showModal.value = false
}

function findEvents(day, slotIndex) {
  return events.value.filter(ev => {
    if (ev.day !== day || ev.allDay) return false
    const sIdx = timeSlots.findIndex(t => t === ev.startTime)
    return sIdx === slotIndex
  })
}

function findAllDayEvents(day) {
  return events.value.filter(ev => ev.day === day && ev.allDay)
}

function calcEventHeight(event) {
  if (event.allDay) return 28
  const startIdx = timeSlots.findIndex(t => t === event.startTime)
  const endIdx = timeSlots.findIndex(t => t === event.endTime)
  const slotHeight = 28
  return (endIdx - startIdx) * slotHeight
}
</script>

<style src="@/assets/calendar.css"></style>
