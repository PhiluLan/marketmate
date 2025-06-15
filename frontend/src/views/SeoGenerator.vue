<template>
  <div class="seo-generator-wrapper">
    <h1 class="headline">SEO-Generator</h1>
    <div class="card-row">
      <!-- 1. Webseiten-Analyse -->
      <div class="card">
        <h2>Live SEO-Analyse</h2>
        <form @submit.prevent="analyzeUrl">
          <label>Webseiten-URL:</label>
          <input v-model="crawlUrl" type="url" class="input" placeholder="https://deine-seite.de" required />
          <button type="submit" class="btn">Analysieren</button>
        </form>
        <div v-if="crawlLoading" class="info">Analyse läuft...</div>
        <div v-if="crawlError" class="error">{{ crawlError }}</div>
        <div v-if="crawlResult && crawlResult.success" class="result">
          <p><b>Titel:</b> {{ crawlResult.title }}</p>
          <p><b>Meta Description:</b> {{ crawlResult.meta_description }}</p>
          <p><b>Anzahl H1:</b> {{ crawlResult.h1_count }}</p>
          <p><b>Anzahl H2:</b> {{ crawlResult.h2_count }}</p>
          <p><b>Wörter insgesamt:</b> {{ crawlResult.word_count }}</p>
        </div>
      </div>

      <!-- 2. KI Meta-Description -->
      <div class="card">
        <h2>KI Meta-Description</h2>
        <form @submit.prevent="generateMeta">
          <label>Seitenname:</label>
          <input v-model="siteName" class="input" placeholder="Kuni-Gunde" required />
          <label>Hauptthema oder Begriffe:</label>
          <input v-model="siteTopic" class="input" placeholder="z.B. Restaurant, Mittagessen, Basel" required />
          <button type="submit" class="btn">Meta Description generieren</button>
        </form>
        <div v-if="metaLoading" class="info">KI denkt nach…</div>
        <div v-if="metaError" class="error">{{ metaError }}</div>
        <div v-if="metaResult" class="result">
          <b>Meta Description:</b>
          <p>{{ metaResult }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/AuthService'

// --- SEO-Analyse (Scrapy) ---
const crawlUrl = ref('')
const crawlLoading = ref(false)
const crawlResult = ref(null)
const crawlError = ref('')

async function analyzeUrl() {
  crawlError.value = ''
  crawlResult.value = null
  crawlLoading.value = true
  try {
    const res = await api.post('/seo/crawl/', { url: crawlUrl.value })
    crawlResult.value = res.data
  } catch (e) {
    crawlError.value = e.response?.data?.detail || 'Fehler beim Crawlen.'
  } finally {
    crawlLoading.value = false
  }
}

// --- KI Meta Description ---
const siteName = ref('')
const siteTopic = ref('')
const metaLoading = ref(false)
const metaResult = ref('')
const metaError = ref('')

async function generateMeta() {
  metaError.value = ''
  metaResult.value = ''
  metaLoading.value = true
  try {
    const res = await api.post('/seo/recommendations/', {
      website_name: siteName.value,
      website_topic: siteTopic.value
    })
    metaResult.value = res.data.recommendation
  } catch (e) {
    metaError.value = e.response?.data?.error || 'Fehler bei der KI-Anfrage.'
  } finally {
    metaLoading.value = false
  }
}
</script>

<style src="@/assets/custom.css"></style>
