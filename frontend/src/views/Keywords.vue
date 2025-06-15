<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Keyword-Tracking & Metriken</h1>

    <!-- Formular zum Anlegen neuer Keywords -->
    <form @submit.prevent="addKeyword" class="mb-4 space-x-2 flex">
      <select v-model="newWebsite" class="border px-2 py-1">
        <option disabled value="">— Website wählen —</option>
        <option v-for="site in websites" :key="site.id" :value="site.id">
          {{ site.name }}
        </option>
      </select>

      <input
        v-model="newTerm"
        placeholder="Keyword (z.B. marketing tool)"
        class="border px-2 py-1 flex-grow"
        required
      />

      <select v-model="newRegion" class="border px-2 py-1">
        <option value="CH">CH</option>
        <option value="DE">DE</option>
        <option value="AT">AT</option>
      </select>

      <button type="submit" class="bg-green-600 text-white px-4 py-1 rounded">
        + Hinzufügen
      </button>
    </form>

    <!-- Tabelle der Keywords, Rankings und Keyword-Metriken -->
    <table class="w-full table-auto border">
      <thead>
        <tr class="bg-gray-200">
          <th class="border px-2">Website</th>
          <th class="border px-2">Keyword</th>
          <th class="border px-2">Region</th>
          <th class="border px-2">Volumen</th>
          <th class="border px-2">Wettbewerb</th>
          <th class="border px-2">Low CPC (€)</th>
          <th class="border px-2">High CPC (€)</th>
          <th class="border px-2">Letzter Rank</th>
          <th class="border px-2">Checked At</th>
          <th class="border px-2">Aktionen</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="kw in keywords" :key="kw.id">
          <td class="border px-2">{{ kw.website_name }}</td>
          <td class="border px-2">{{ kw.term }}</td>
          <td class="border px-2">{{ kw.region }}</td>
          <td class="border px-2">{{ kw.monthly_searches ?? '–' }}</td>
          <td class="border px-2">{{ kw.competition ?? '–' }}</td>
          <td class="border px-2">
            {{ kw.low_cpc != null ? kw.low_cpc.toFixed(2) : '–' }}
          </td>
          <td class="border px-2">
            {{ kw.high_cpc != null ? kw.high_cpc.toFixed(2) : '–' }}
          </td>
          <td class="border px-2">
            {{ kw.latest.length ? kw.latest[0].rank : '–' }}
          </td>
          <td class="border px-2">
            {{ kw.latest.length
              ? new Date(kw.latest[0].checked_at).toLocaleString()
              : '–' }}
          </td>
          <td class="border px-2 space-x-2">
            <button
              @click="checkRanking(kw.id)"
              class="bg-blue-600 text-white px-2 py-1 rounded"
            >
              Neu prüfen
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api.js'  // zentrale Axios-Instanz

// Reactive State
const websites   = ref([])
const keywords   = ref([])
const metrics    = ref([])
const metricsMap = ref({})

const newWebsite = ref('')
const newTerm    = ref('')
const newRegion  = ref('CH')

// Korrekte Endpunkte relativ zu baseURL=http://localhost:8000/api
const WS_ENDPOINT      = 'websites/'           // GET, POST → /api/websites/
const KW_ENDPOINT      = 'keywords/keywords/'  // GET, POST → /api/keywords/keywords/
const METRICS_ENDPOINT = 'keywords/metrics/'   // GET → /api/keywords/metrics/

// Websites laden
async function fetchWebsites() {
  try {
    const { data } = await api.get(WS_ENDPOINT)
    websites.value = data
  } catch (err) {
    console.error('Fehler fetchWebsites', err.response?.status, err.response?.data)
  }
}

// Keywords laden
async function fetchKeywords() {
  try {
    const { data } = await api.get(KW_ENDPOINT)
    keywords.value = data.map(kw => ({
      ...kw,
      website_name: websites.value.find(w => w.id === kw.website)?.name || '–'
    }))
  } catch (err) {
    console.error('Fehler fetchKeywords', err.response?.status, err.response?.data)
  }
}

// Keyword-Metriken laden
async function fetchMetrics() {
  try {
    const { data } = await api.get(METRICS_ENDPOINT)
    metrics.value = data
    const map = {}
    data.forEach(m => { map[m.keyword] = m })
    metricsMap.value = map
  } catch (err) {
    console.error('Fehler fetchMetrics', err.response?.status, err.response?.data)
  }
}

// Metrics in Keywords einfügen
function mergeMetrics() {
  keywords.value = keywords.value.map(kw => {
    const m = metricsMap.value[kw.term] || {}
    return {
      ...kw,
      monthly_searches: m.monthly_searches ?? null,
      competition:      m.competition      ?? null,
      low_cpc:          m.low_cpc          ?? null,
      high_cpc:         m.high_cpc         ?? null
    }
  })
}

// Neues Keyword anlegen
async function addKeyword() {
  if (!newWebsite.value) {
    alert('Bitte eine Website auswählen.')
    return
  }
  try {
    await api.post(KW_ENDPOINT, {
      website: newWebsite.value,
      term:    newTerm.value,
      region:  newRegion.value
    })
    newTerm.value    = ''
    newWebsite.value = ''
    await reloadAll()
  } catch (err) {
    console.error('Fehler addKeyword', err.response?.status, err.response?.data)
  }
}

// Ranking-Check
async function checkRanking(id) {
  try {
    await api.post(`${KW_ENDPOINT}${id}/check/`)
    await reloadAll()
  } catch (err) {
    console.error('Fehler checkRanking', err.response?.status, err.response?.data)
  }
}

// Alles neu laden: Websites → Keywords → Metrics → Merge
async function reloadAll() {
  await fetchWebsites()
  await fetchKeywords()
  await fetchMetrics()
  mergeMetrics()
}

onMounted(reloadAll)
</script>

<style scoped>
/* optional eigene Styles */
</style>
