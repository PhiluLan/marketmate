<template>
  <div class="analysis-page">
    <!-- 1) Headline -->
    <h1 class="headline">
      Hallo {{ firstName }}! Dein erster heyLenny Check von {{ websiteUrl }}
    </h1>

    <!-- 2) Loading / Error -->
    <p v-if="loading" class="loading">
      Bitte warten… wir analysieren deine Seite im Hintergrund!
    </p>
    <p v-else-if="error" class="error">{{ error }}</p>

    <!-- 3) Audit läuft noch -->
    <div v-else-if="!auditComplete" class="waiting">
      Dein Audit läuft noch. Bitte <button @click="reload">hier neu laden</button>.
    </div>

    <!-- 4) Fertige Summary + Metriken + Social -->
    <div v-else>
      <!-- Zusammenfassung -->
      <section class="summary-section" v-html="formattedSummary"></section>

      <!-- SEO-Metriken -->
      <section class="metrics-section">
        <div class="metrics-group">
          <h2>Top 4 Werte</h2>
          <div class="metrics-grid">
            <div v-for="m in topMetrics" :key="m.label" class="metric-box top">
              <span class="metric-label">{{ m.label }}</span>
              <span class="metric-value">{{ m.value }}</span>
            </div>
          </div>
        </div>
        <div class="metrics-group">
          <h2>Top 4 Baustellen</h2>
          <div class="metrics-grid">
            <div v-for="m in poorMetrics" :key="m.label" class="metric-box poor">
              <span class="metric-label">{{ m.label }}</span>
              <span class="metric-value">{{ m.value }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Social-Media-Daten -->
      <section v-if="socialSummary" class="social-section">
        <h2>Social Media Insights</h2>
        <div class="social-grid">
          <!-- Instagram -->
          <div v-if="socialSummary.instagram" class="social-box">
            <h3>Instagram</h3>
            <p>Follower: {{ socialSummary.instagram.followers ?? '–' }}</p>
            <p>Ø Likes: {{ socialSummary.instagram.avg_likes ?? '–' }}</p>
            <p>Ø Kommentare: {{ socialSummary.instagram.avg_comments ?? '–' }}</p>
          </div>
          <!-- Facebook -->
          <div v-if="socialSummary.facebook" class="social-box">
            <h3>Facebook</h3>
            <p>Follower: {{ socialSummary.facebook.followers ?? '–' }}</p>
            <p>Ø Likes: {{ socialSummary.facebook.avg_likes ?? '–' }}</p>
            <p>Ø Kommentare: {{ socialSummary.facebook.avg_comments ?? '–' }}</p>
          </div>
          <!-- LinkedIn -->
          <div v-if="socialSummary.linkedin" class="social-box">
            <h3>LinkedIn</h3>
            <p>Follower: {{ socialSummary.linkedin.followers ?? '–' }}</p>
            <p>Ø Likes: {{ socialSummary.linkedin.avg_likes ?? '–' }}</p>
            <p>Ø Kommentare: {{ socialSummary.linkedin.avg_comments ?? '–' }}</p>
          </div>
        </div>
      </section>

      <!-- Weiter-Button -->
      <button class="continue-btn" @click="goToDashboard">
        Zur Dashboard-Übersicht
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/api.js'

const route       = useRoute()
const router      = useRouter()
const token       = route.query.token || ''
const loading     = ref(true)
const error       = ref(null)
const firstName   = ref('–')
const websiteUrl  = ref('–')
const formattedSummary = ref('')
const topMetrics  = ref([])
const poorMetrics = ref([])
const auditComplete = ref(false)
// neu:
const socialSummary = ref(null)

// holt die Daten vom Backend
async function fetchData() {
  try {
    const { data } = await api.get(`/users/verify-email/?token=${token}`)
    firstName.value      = data.first_name
    websiteUrl.value     = data.website_url
    formattedSummary.value = data.hey_lenny_summary
      .split('\n')
      .map(l => `<p>${l}</p>`)
      .join('')
    topMetrics.value     = data.top_metrics
    poorMetrics.value    = data.poor_metrics
    auditComplete.value  = data.audit_complete
    socialSummary.value  = data.social_summary  // hier setzen
  } catch (e) {
    error.value = e.response?.data?.detail || 'Verifikation fehlgeschlagen.'
  } finally {
    loading.value = false
  }
}

// manuelles Nachladen
function reload() {
  loading.value = true
  fetchData()
}

// Weiterleitung
function goToDashboard() {
  router.push('/dashboard')
}

onMounted(() => {
  if (!token) {
    error.value   = 'Kein Token gefunden.'
    loading.value = false
  } else {
    fetchData()
  }
})
</script>

<style src="@/assets/VerifyEmail.css"></style>
