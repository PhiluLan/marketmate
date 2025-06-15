<template>
  <div class="marketmate-dashboard-container">
    <!-- Kopfzeile -->
    <div class="dashboard-header">
      <div>
        <h1 class="dashboard-title">MarketMate Dashboard</h1>
        <span class="dashboard-subtitle">Dein Online Marketing Überblick</span>
      </div>
      <!-- Webseiten Dropdown -->
      <div class="dashboard-site-select">
        <label class="font-semibold">Webseite:</label>
        <select
          v-model="selectedWebsiteId"
          @change="reloadAll"
        >
          <option v-for="site in websites" :key="site.id" :value="site.id">
            {{ site.name || site.url }}
          </option>
        </select>
        <router-link
          to="/websites/add"
          class="add-btn"
        >+ Neue Website</router-link>
      </div>
    </div>

    <!-- Dash Karten -->
    <div class="dash-cards">
      <!-- SEO Score -->
      <div class="dash-card">
        <span class="card-label">SEO Score</span>
        <span class="card-value green">
          {{ audits.length && audits[0]?.score != null ? audits[0].score + '/100' : '-' }}
        </span>
        <span class="card-sub">
          Letzter Audit:
          <template v-if="audits.length && audits[0]?.created_at">
            {{ new Date(audits[0].created_at).toLocaleString() }}
          </template>
          <template v-else>—</template>
        </span>
      </div>
      <!-- Keyword Ranking -->
      <div class="dash-card">
        <span class="card-label">Top-Keyword</span>
        <span class="card-value blue">
          {{ keywords.length > 0 ? keywords[0].term || keywords[0].keyword || '—' : '—' }}
        </span>
        <span class="card-sub">
          Platz {{ keywords.length > 0 ? (keywords[0].rank ?? '-') : '-' }}
        </span>
      </div>
      <!-- Performance -->
      <div class="dash-card">
        <span class="card-label">Performance</span>
        <span class="card-value yellow">
          {{ audits.length && audits[0]?.load_time ? audits[0].load_time + ' ms' : '-' }}
        </span>
        <span class="card-sub">Ladezeit</span>
      </div>
      <!-- Fehler -->
      <div class="dash-card">
        <span class="card-label">OnPage Fehler</span>
        <span class="card-value red">
          {{ audits.length && audits[0]?.broken_links != null ? audits[0].broken_links : '-' }}
        </span>
        <span class="card-sub">Broken Links</span>
      </div>
    </div>

    <!-- KI Empfehlung meta Beschreibung -->
    <div class="ki-widget">
  <h2 class="ki-widget-title">KI-Empfehlung: Meta-Description</h2>
  <div v-if="recLoading" class="ki-widget-loading">KI denkt nach...</div>
  <div v-else-if="recommendation" class="ki-widget-recommendation">
    {{ recommendation }}
  </div>
  <button
    @click="fetchRecommendation"
    class="ki-widget-btn"
    :disabled="recLoading"
  >
    Neue Empfehlung generieren
  </button>
</div>


    <!-- Listenbereich -->
    <div class="dash-lists">
      <!-- Audits Liste -->
      <div class="dash-list-block">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 9px;">
          <h2>Letzte SEO-Audits</h2>
          <button
            @click="triggerAudit"
            class="block-action-btn"
          >SEO-Audit starten</button>
        </div>
        <ul>
          <li
            v-for="audit in audits"
            :key="audit.id"
          >
            <span>{{ audit.created_at ? new Date(audit.created_at).toLocaleString() : '—' }}</span>
            <span style="font-weight:600;">{{ audit.score != null ? audit.score + '/100' : '-' }}</span>
            <router-link
              :to="`/seo/${selectedWebsiteId}`"
              style="color: #2563eb; text-decoration: underline; font-size:0.98rem; margin-left:9px;"
            >Details</router-link>
          </li>
          <li v-if="audits.length === 0" class="empty">Keine Audits gefunden.</li>
        </ul>
      </div>
      <!-- Keywords Liste -->
      <div class="dash-list-block">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 9px;">
          <h2>Aktuelle Keywords</h2>
          <router-link
            :to="`/seo/${selectedWebsiteId}`"
            class="block-action-btn"
          >Keyword hinzufügen</router-link>
        </div>
        <ul>
          <li
            v-for="kw in keywords"
            :key="kw.id"
          >
            <span>{{ kw.term || kw.keyword }}</span>
            <span style="color:#6b7280;">Platz {{ kw.rank ?? '-' }}</span>
          </li>
          <li v-if="keywords.length === 0" class="empty">Keine Keywords vorhanden.</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/AuthService'
import { useRouter } from 'vue-router'

const websites = ref([])
const selectedWebsiteId = ref(null)
const detail = ref(null)
const error = ref(null)
const loading = ref(true)
const recommendation = ref('')
const recLoading = ref(false)
const router = useRouter()

const audits = computed(() => detail.value?.audits || [])
const keywords = computed(() => detail.value?.keywords || [])

function reloadAll() {
  fetchWebsiteData()
}

// Holt alle Websites und initialisiert Auswahl
async function fetchWebsites() {
  loading.value = true
  try {
    const res = await api.get('/websites/')
    websites.value = res.data
    if (websites.value.length && !selectedWebsiteId.value) {
      selectedWebsiteId.value = websites.value[0].id
      await fetchWebsiteData()
    }
  } catch (e) {
    error.value = 'Fehler beim Laden der Websites'
  } finally {
    loading.value = false
  }
}

// Holt Detaildaten (Audits, Keywords) für die gewählte Website
async function fetchWebsiteData() {
  if (!selectedWebsiteId.value) return
  loading.value = true
  try {
    const res = await api.get(`/seo/detail/?website_id=${selectedWebsiteId.value}`)
    detail.value = res.data
    error.value = null
    recommendation.value = ''
  } catch (e) {
    error.value = 'Fehler beim Laden der Website-Daten'
    detail.value = null
  } finally {
    loading.value = false
  }
}

async function triggerAudit() {
  if (!selectedWebsiteId.value) return
  loading.value = true
  try {
    await api.post('/seo/audit/run/', { website_id: selectedWebsiteId.value })
    await fetchWebsiteData() // Neu laden!
  } catch {
    error.value = 'Audit konnte nicht gestartet werden.'
  } finally {
    loading.value = false
  }
}

async function fetchRecommendation() {
  if (!detail.value || !detail.value.website) return;
  recLoading.value = true;
  try {
    const res = await api.post('/seo/recommendations/', {
      website_name: detail.value.website.name,
      website_topic: 'SEO Optimierung' // Oder dynamisch aus anderem Feld!
    });
    recommendation.value = res.data.recommendation;
  } catch {
    recommendation.value = 'Fehler beim Abrufen der KI-Empfehlung';
  } finally {
    recLoading.value = false;
  }
}

onMounted(() => fetchWebsites())
</script>
