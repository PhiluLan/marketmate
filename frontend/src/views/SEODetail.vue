<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/AuthService.js'
import { useRoute } from 'vue-router'

const route = useRoute()
const websiteId = route.params.id
const loading = ref(true)
const detail = ref(null)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await api.get(`/seo/detail/?website_id=${websiteId}`)
    detail.value = res.data
  } catch (e) {
    error.value = 'Fehler beim Laden der SEO-Details'
  } finally {
    loading.value = false
  }
})

const triggerAudit = async () => {
  try {
    await api.post('/seo/audit/run/', { website_id: websiteId })
    window.location.reload()
  } catch {
    alert('Audit konnte nicht gestartet werden.')
  }
}

const newKeyword = ref('')
const addingKeyword = ref(false)

const addKeyword = async () => {
  if (!newKeyword.value.trim()) return
  addingKeyword.value = true
  try {
    await api.post('/keywords/', {
      website: websiteId,
      term: newKeyword.value,
      region: 'de' // oder '' wenn du keine Region brauchst
    })
    newKeyword.value = ''
    // Keywords neu laden!
    await reloadDetail()
  } catch {
    alert('Keyword konnte nicht gespeichert werden.')
  } finally {
    addingKeyword.value = false
  }
}

// Hilfsfunktion zum Neuladen:
async function reloadDetail() {
  try {
    const res = await api.get(`/seo/detail/?website_id=${websiteId}`)
    detail.value = res.data
  } catch (e) {
    error.value = 'Fehler beim Laden der SEO-Details'
  }
}

</script>

<template>
  <div class="max-w-4xl mx-auto p-4">
    <h1 class="text-2xl mb-2">
      SEO-Detail: {{ detail?.website?.name || detail?.website?.url || '' }}
    </h1>
    <div v-if="loading">Lade Daten...</div>
    <div v-if="error" class="text-red-600">{{ error }}</div>
    <div v-if="detail">
      <div class="bg-white p-4 rounded shadow mb-4">
        <p><strong>Domain:</strong> {{ detail.website.url }}</p>
        <p>
          <strong>Letzter Audit:</strong>
          {{ detail.audits?.[0]?.created_at ? new Date(detail.audits[0].created_at).toLocaleString() : '—' }}
        </p>
        <button
          @click="triggerAudit"
          class="mt-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
        >SEO-Audit starten</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h2 class="font-semibold mb-2">Letzte Audits</h2>
          <ul>
            <li v-if="detail.audits?.length === 0" class="text-gray-500">Keine Audits vorhanden.</li>
            <li
              v-for="audit in detail.audits"
              :key="audit.id"
              class="border-b py-2"
            >
              {{ new Date(audit.created_at).toLocaleString() }} – Score: {{ audit.seo_score ?? audit.score ?? '-' }}
            </li>
          </ul>
        </div>
        <div>
          <h2 class="font-semibold mb-2">Aktuelle Keywords</h2>
          <div class="flex gap-2 mb-2">
            <input
                v-model="newKeyword"
                placeholder="Neues Keyword eingeben"
                class="border px-2 py-1 rounded flex-1"
                :disabled="addingKeyword"
                @keyup.enter="addKeyword"
            >
            <button
                @click="addKeyword"
                class="bg-blue-600 text-white px-3 py-1 rounded"
                :disabled="addingKeyword"
                >Speichern</button>
            </div>

          <ul>
            <li v-if="!detail.keywords || detail.keywords.length === 0" class="text-gray-500">Keine Keywords erfasst.</li>
            <li
              v-for="kw in detail.keywords"
              :key="kw.id"
              class="border-b py-2"
            >
              {{ kw.term }}: Platz {{ kw.rank ?? '-' }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Hier kann später das KI-Widget zur Meta-Description eingebaut werden! -->
    </div>
  </div>
</template>
