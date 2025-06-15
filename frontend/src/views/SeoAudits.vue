<template>
  <div class="seo-detail-container">
    <h1 class="seo-detail-headline">SEO-Analyse für {{ websiteName || 'Website' }}</h1>

    <div class="seo-detail-toolbar">
      <label for="websiteSelect" class="seo-detail-label">Website:</label>
      <select id="websiteSelect" v-model="selectedWebsiteId" @change="reloadAudit" class="seo-detail-select">
        <option v-for="site in websites" :key="site.id" :value="site.id">{{ site.name || site.url }}</option>
      </select>
      <button class="seo-detail-btn" @click="runAudit" :disabled="auditRunning">
        {{ auditRunning ? 'Audit läuft...' : 'Audit starten' }}
      </button>
    </div>

    <div class="seo-cards-grid">
      <!-- Meta Title -->
      <div class="seo-card">
        <div class="seo-card-title">Meta Title</div>
        <div class="seo-card-value">{{ audit.meta_title || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClass(audit.meta_title, 60, 10)">
            {{ ampelText(audit.meta_title, 60, 10) }}
          </span>
          <span v-if="audit.meta_title">({{ audit.meta_title.length }}/60 Zeichen)</span>
        </div>
      </div>
      <!-- Meta Description -->
      <div class="seo-card">
        <div class="seo-card-title">Meta Description</div>
        <div class="seo-card-value">{{ audit.meta_description || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClass(audit.meta_description, 155, 50)">
            {{ ampelText(audit.meta_description, 155, 50) }}
          </span>
          <span v-if="audit.meta_description">({{ audit.meta_description.length }}/155 Zeichen)</span>
        </div>
      </div>
      <!-- Meta Robots -->
      <div class="seo-card">
        <div class="seo-card-title">Meta Robots</div>
        <div class="seo-card-value">{{ audit.meta_robots || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClass(audit.meta_robots, 30, 5)">
            {{ ampelText(audit.meta_robots, 30, 5) }}
          </span>
        </div>
      </div>
      <!-- Canonical -->
      <div class="seo-card">
        <div class="seo-card-title">Canonical</div>
        <div class="seo-card-value">{{ audit.canonical || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.canonical ? 'ampel gruen' : 'ampel rot'">
            {{ audit.canonical ? '🟢 Vorhanden' : '❌ Fehlend' }}
          </span>
        </div>
      </div>
      <!-- H1/H2 Count -->
      <div class="seo-card">
        <div class="seo-card-title">H1 / H2 Überschriften</div>
        <div class="seo-card-value">H1: {{ audit.h1_count ?? '-' }}, H2: {{ audit.h2_count ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.h1_count === 1 ? 'ampel gruen' : 'ampel rot'">
            {{ audit.h1_count === 1 ? '🟢 1x H1' : '❌ Nicht optimal' }}
          </span>
        </div>
      </div>

            <!-- H3 / H4 / H5 / H6 Überschriften -->
      <div class="seo-card">
        <div class="seo-card-title">H3–H6 Überschriften</div>
        <div class="seo-card-value">
          H3: {{ audit.h3_count ?? '-' }},
          H4: {{ audit.h4_count ?? '-' }},
          H5: {{ audit.h5_count ?? '-' }},
          H6: {{ audit.h6_count ?? '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="(audit.h3_count > 0 && audit.h3_count <= 3)
                      && (audit.h4_count <= audit.h3_count)
                      ? 'ampel gruen'
                      : 'ampel gelb'">
            {{ (audit.h3_count > 0 && audit.h3_count <= 3)
              && (audit.h4_count <= audit.h3_count)
              ? '🟢 Struktur OK'
              : '🟡 Struktur prüfen' }}
          </span>
        </div>
      </div>

            <!-- Flesch-Reading-Ease Score -->
      <div class="seo-card">
        <div class="seo-card-title">Lesbarkeits-Score (Flesch)</div>
        <div class="seo-card-value">
          {{ audit.reading_score != null ? audit.reading_score.toFixed(2) : '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.reading_score != null
              ? (audit.reading_score >= 60
                  ? 'ampel gruen'
                  : audit.reading_score >= 50
                    ? 'ampel gelb'
                    : 'ampel rot')
              : 'ampel rot'">
            {{ audit.reading_score != null
              ? (audit.reading_score >= 60
                  ? '🟢 Leicht lesbar'
                  : audit.reading_score >= 50
                    ? '🟡 Mittel'
                    : '❌ Schwer lesbar')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <!-- Keyword-Dichte -->
      <div class="seo-card">
        <div class="seo-card-title">Keyword-Dichte (%)</div>
        <div class="seo-card-value">
          {{ audit.keyword_density != null
            ? audit.keyword_density.toFixed(2) + '%'
            : '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.keyword_density != null
              ? (audit.keyword_density >= 1 && audit.keyword_density <= 3
                  ? 'ampel gruen'
                  : 'ampel gelb')
              : 'ampel rot'">
            {{ audit.keyword_density != null
              ? (audit.keyword_density >= 1 && audit.keyword_density <= 3
                  ? '🟢 Optimal'
                  : '🟡 Außerhalb empfohlen')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <!-- Word Count -->
      <div class="seo-card">
        <div class="seo-card-title">Word Count</div>
        <div class="seo-card-value">{{ audit.word_count ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClassNum(audit.word_count, 150, 50)">
            {{ ampelTextNum(audit.word_count, 150, 50) }}
          </span>
        </div>
      </div>
      <!-- OG Title -->
      <div class="seo-card">
        <div class="seo-card-title">OG Title</div>
        <div class="seo-card-value">{{ audit.og_title || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.og_title ? 'ampel gruen' : 'ampel rot'">
            {{ audit.og_title ? '🟢 Vorhanden' : '❌ Fehlend' }}
          </span>
        </div>
      </div>
      <!-- OG Description -->
      <div class="seo-card">
        <div class="seo-card-title">OG Description</div>
        <div class="seo-card-value">{{ audit.og_description || '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.og_description ? 'ampel gruen' : 'ampel rot'">
            {{ audit.og_description ? '🟢 Vorhanden' : '❌ Fehlend' }}
          </span>
        </div>
      </div>
      <!-- Ladezeit -->
      <div class="seo-card">
        <div class="seo-card-title">Ladezeit</div>
        <div class="seo-card-value">{{ audit.load_time }} ms</div>
        <div class="seo-card-ampel">
          <span :class="ampelClassNum(audit.load_time, 1500, 400, true)">
            {{ ampelTextNum(audit.load_time, 1500, 400, true) }}
          </span>
        </div>
      </div>
      <!-- Broken Links -->
      <div class="seo-card">
        <div class="seo-card-title">Broken Links</div>
        <div class="seo-card-value">{{ audit.broken_links }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.broken_links === 0 ? 'ampel gruen' : audit.broken_links < 3 ? 'ampel gelb' : 'ampel rot'">
            {{ audit.broken_links === 0 ? '🟢 Keine' : audit.broken_links < 3 ? '🟡 Wenige' : '❌ Viele' }}
          </span>
        </div>
      </div>

      <!-- First Contentful Paint -->
      <div class="seo-card">
        <div class="seo-card-title">FCP (ms)</div>
        <div class="seo-card-value">{{ audit.fcp?.toFixed(0) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClassNum(audit.fcp, 2500, 1000, true)">
            {{ ampelTextNum(audit.fcp, 2500, 1000, true) }}
          </span>
        </div>
      </div>

      <!-- Largest Contentful Paint -->
      <div class="seo-card">
        <div class="seo-card-title">LCP (ms)</div>
        <div class="seo-card-value">{{ audit.lcp?.toFixed(0) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClassNum(audit.lcp, 2500, 1500, true)">
            {{ ampelTextNum(audit.lcp, 2500, 1500, true) }}
          </span>
        </div>
      </div>

      <!-- Cumulative Layout Shift -->
      <div class="seo-card">
        <div class="seo-card-title">CLS</div>
        <div class="seo-card-value">{{ audit.cls?.toFixed(2) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.cls <= 0.1 ? 'ampel gruen' : audit.cls <= 0.25 ? 'ampel gelb' : 'ampel rot'">
            {{ audit.cls <= 0.1 ? '🟢 Gut' : audit.cls <= 0.25 ? '🟡 OK' : '❌ Schlecht' }}
          </span>
        </div>
      </div>

      <!-- Time to Interactive -->
      <div class="seo-card">
        <div class="seo-card-title">TTI (ms)</div>
        <div class="seo-card-value">{{ audit.tti?.toFixed(0) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="ampelClassNum(audit.tti, 5000, 3000, true)">
            {{ ampelTextNum(audit.tti, 5000, 3000, true) }}
          </span>
        </div>
      </div>
      <!-- SEO Score -->
      <div class="seo-card">
        <div class="seo-card-title">SEO Score</div>
        <div class="seo-card-value">{{ audit.score }}/100</div>
        <div class="seo-card-ampel">
          <span :class="audit.score >= 80 ? 'ampel gruen' : audit.score >= 50 ? 'ampel gelb' : 'ampel rot'">
            {{ audit.score >= 80 ? '🟢 Sehr gut' : audit.score >= 50 ? '🟡 Mittel' : '❌ Niedrig' }}
          </span>
        </div>
      </div>

            <!-- SSL-Zertifikat -->
      <div class="seo-card">
        <div class="seo-card-title">SSL gültig bis</div>
        <div class="seo-card-value">
          {{ audit.ssl_valid_until
            ? new Date(audit.ssl_valid_until).toLocaleDateString()
            : '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.ssl_valid_until && new Date(audit.ssl_valid_until) > new Date()
            ? 'ampel gruen'
            : 'ampel rot'">
            {{ audit.ssl_valid_until && new Date(audit.ssl_valid_until) > new Date()
              ? '🟢 Gültig'
              : '❌ Abgelaufen' }}
          </span>
        </div>
      </div>

      <!-- Security-Header -->
      <div class="seo-card">
        <div class="seo-card-title">Security-Header</div>
        <div class="seo-card-value">
          <div>HSTS: 
            <span :class="audit.hsts ? 'text-green-600' : 'text-red-600'">
              {{ audit.hsts ? 'Ja' : 'Nein' }}
            </span>
          </div>
          <div>CSP:  
            <span :class="audit.csp ? 'text-green-600' : 'text-red-600'">
              {{ audit.csp ? 'Ja' : 'Nein' }}
            </span>
          </div>
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.hsts && audit.csp
            ? 'ampel gruen'
            : 'ampel rot'">
            {{ audit.hsts && audit.csp
              ? '🟢 Alle vorhanden'
              : '❌ Fehlende Header' }}
          </span>
        </div>
      </div>

            <!-- robots.txt -->
      <div class="seo-card">
        <div class="seo-card-title">robots.txt</div>
        <div class="seo-card-value">
          <span :class="audit.robots_directives ? 'ampel gruen' : 'ampel rot'">
            {{ audit.robots_directives ? '🟢 Gefunden' : '❌ Fehlend' }}
          </span>
        </div>
        <details v-if="audit.robots_directives">
          <summary>Direktiven anzeigen</summary>
          <pre class="overflow-auto">{{ audit.robots_directives }}</pre>
        </details>
      </div>

      <!-- Sitemap -->
      <div class="seo-card">
        <div class="seo-card-title">Sitemap</div>
        <div class="seo-card-value">
          <span :class="audit.sitemap_valid ? 'ampel gruen' : 'ampel rot'">
            {{ audit.sitemap_valid ? '🟢 Valid' : '❌ Ungültig' }}
          </span>
        </div>
        <details v-if="audit.sitemap_errors">
          <summary>Fehler anzeigen</summary>
          <pre class="overflow-auto">{{ audit.sitemap_errors }}</pre>
        </details>
      </div>

            <!-- JavaScript-Rendering -->
      <div class="seo-card">
        <div class="seo-card-title">JS-Rendering</div>
        <div class="seo-card-value">
          <span :class="audit.js_render_blocking_resources ? 'ampel gruen' : 'ampel rot'">
            {{ audit.js_render_blocking_resources ? '🟢 Gefunden' : '❌ Keine Skripte' }}
          </span>
        </div>
        <details v-if="audit.js_render_blocking_resources">
          <summary>
            Skripte anzeigen ({{ JSON.parse(audit.js_render_blocking_resources).length }})
          </summary>
          <pre class="overflow-auto">{{ audit.js_render_blocking_resources }}</pre>
        </details>
      </div>

            <!-- Title-Tag-Check -->
      <div class="seo-card">
        <div class="seo-card-title">Title-Länge</div>
        <div class="seo-card-value">{{ audit.title_length ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.title_length >= 50 && audit.title_length <= 60
              ? 'ampel gruen'
              : audit.title_length
                ? 'ampel gelb'
                : 'ampel rot'">
            {{ audit.title_length
              ? (audit.title_length >= 50 && audit.title_length <= 60
                  ? '🟢 Optimal'
                  : '🟡 Nicht optimal')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

            <!-- Meta-Description-Länge -->
      <div class="seo-card">
        <div class="seo-card-title">Meta-Description-Länge</div>
        <div class="seo-card-value">{{ audit.meta_description_length ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.meta_description_length >= 120 && audit.meta_description_length <= 155
              ? 'ampel gruen'
              : audit.meta_description_length
                ? 'ampel gelb'
                : 'ampel rot'">
            {{ audit.meta_description_length
              ? (audit.meta_description_length >= 120 && audit.meta_description_length <= 155
                  ? '🟢 Optimal'
                  : '🟡 Nicht optimal')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <!-- Meta-Description-Einzigartigkeit -->
      <div class="seo-card">
        <div class="seo-card-title">Meta-Description eindeutig</div>
        <div class="seo-card-value">
          {{ audit.meta_description_unique === true
            ? 'Ja'
            : audit.meta_description_unique === false
              ? 'Nein'
              : '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.meta_description_unique === true
              ? 'ampel gruen'
              : audit.meta_description_unique === false
                ? 'ampel rot'
                : 'ampel rot'">
            {{ audit.meta_description_unique === true
              ? '🟢 Einzigartig'
              : audit.meta_description_unique === false
                ? '❌ Duplikat'
                : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <div class="seo-card">
        <div class="seo-card-title">Keyword-Position</div>
        <div class="seo-card-value">
          {{ audit.title_keyword_position != null
            ? (audit.title_keyword_position > 0
                ? audit.title_keyword_position
                : 'Nicht gefunden')
            : '-' }}
        </div>
        <div class="seo-card-ampel">
          <span :class="audit.title_keyword_position > 0
              ? 'ampel gruen'
              : audit.title_keyword_position === 0
                ? 'ampel rot'
                : 'ampel rot'">
            {{ audit.title_keyword_position > 0
              ? '🟢 Gefunden'
              : audit.title_keyword_position === 0
                ? '❌ Nicht gefunden'
                : '❌ Fehlend' }}
          </span>
        </div>
      </div>


        <div class="seo-card">
  <div class="seo-card-title">HTTP Status Code</div>
  <div class="seo-card-value">{{ audit.http_status ?? '-' }}</div>
  <div class="seo-card-ampel">
    <span :class="audit.http_status === 200 ? 'ampel gruen' : 'ampel rot'">
      {{ audit.http_status === 200 ? '🟢 OK' : '❌ Fehler' }}
    </span>
  </div>
</div>

      <!-- Duplicate-Content (Intra-Site) -->
      <div class="seo-card">
        <div class="seo-card-title">Duplicate-Content</div>
        <div class="seo-card-value">
          <span :class="audit.duplicate_sections
                ? 'ampel rot'
                : 'ampel gruen'">
            {{ audit.duplicate_sections
              ? '❌ Duplikate gefunden'
              : '🟢 Keine Duplikate' }}
          </span>
        </div>
        <details v-if="audit.duplicate_sections">
          <summary>Duplizierte Absätze anzeigen</summary>
          <pre class="overflow-auto">{{ audit.duplicate_sections }}</pre>
        </details>
      </div>

            <!-- Backlink-Gesamtzahl -->
      <div class="seo-card">
        <div class="seo-card-title">Backlinks gesamt</div>
        <div class="seo-card-value">{{ audit.backlink_count ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.backlink_count != null
              ? (audit.backlink_count >= 100
                  ? 'ampel gruen'
                  : audit.backlink_count >= 10
                    ? 'ampel gelb'
                    : 'ampel rot')
              : 'ampel rot'">
            {{ audit.backlink_count != null
              ? (audit.backlink_count >= 100
                  ? '🟢 Sehr viele'
                  : audit.backlink_count >= 10
                    ? '🟡 Mittel'
                    : '❌ Wenige')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <!-- Referring Domains -->
      <div class="seo-card">
        <div class="seo-card-title">Referring Domains</div>
        <div class="seo-card-value">{{ audit.referring_domains ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.referring_domains != null
              ? (audit.referring_domains >= 50
                  ? 'ampel gruen'
                  : audit.referring_domains >= 5
                    ? 'ampel gelb'
                    : 'ampel rot')
              : 'ampel rot'">
            {{ audit.referring_domains != null
              ? (audit.referring_domains >= 50
                  ? '🟢 Viele'
                  : audit.referring_domains >= 5
                    ? '🟡 Wenige'
                    : '❌ Sehr wenige')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

            <!-- Domain Authority -->
      <div class="seo-card">
        <div class="seo-card-title">Domain Authority</div>
        <div class="seo-card-value">{{ audit.domain_authority?.toFixed(1) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.domain_authority != null
              ? (audit.domain_authority >= 60
                  ? 'ampel gruen'
                  : audit.domain_authority >= 40
                    ? 'ampel gelb'
                    : 'ampel rot')
              : 'ampel rot'">
            {{ audit.domain_authority != null
              ? (audit.domain_authority >= 60
                  ? '🟢 Hoch'
                  : audit.domain_authority >= 40
                    ? '🟡 Mittel'
                    : '❌ Niedrig')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

      <!-- Trust Score (Spam Score) -->
      <div class="seo-card">
        <div class="seo-card-title">Trust Score</div>
        <div class="seo-card-value">{{ audit.trust_score?.toFixed(1) ?? '-' }}</div>
        <div class="seo-card-ampel">
          <span :class="audit.trust_score != null
              ? (audit.trust_score <= 3
                  ? 'ampel gruen'
                  : audit.trust_score <= 10
                    ? 'ampel gelb'
                    : 'ampel rot')
              : 'ampel rot'">
            {{ audit.trust_score != null
              ? (audit.trust_score <= 3
                  ? '🟢 Gering'
                  : audit.trust_score <= 10
                    ? '🟡 Mittel'
                    : '❌ Hoch')
              : '❌ Fehlend' }}
          </span>
        </div>
      </div>

            <!-- Ankertext-Verteilung -->
      <div class="seo-card">
        <div class="seo-card-title">Top 5 Ankertexte</div>
        <div class="seo-card-value">
          <span :class="audit.anchor_text_distribution
                ? 'ampel gruen'
                : 'ampel rot'">
            {{ audit.anchor_text_distribution
              ? '🟢 Vorhanden'
              : '❌ Keine Daten' }}
          </span>
        </div>
        <details v-if="audit.anchor_text_distribution">
          <summary>Ankertexte anzeigen</summary>
          <pre class="overflow-auto">{{ audit.anchor_text_distribution }}</pre>
        </details>
      </div>




    </div>

    <div class="seo-detail-datum">Letzter Audit: <b>{{ audit.created_at ? new Date(audit.created_at).toLocaleString() : '-' }}</b></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/api.js'

const websites = ref([])
const selectedWebsiteId = ref(null)
const audit = ref({})
const websiteName = ref('')
const auditRunning = ref(false)

async function fetchWebsites() {
  const res = await api.get('/websites/')
  websites.value = res.data
  if (!selectedWebsiteId.value && websites.value.length) {
    selectedWebsiteId.value = websites.value[0].id
    await fetchAudit()
  }
}

async function fetchAudit() {
  if (!selectedWebsiteId.value) return
  const res = await api.get('/seo/', { params: { website_id: selectedWebsiteId.value } })
  audit.value = res.data.length ? res.data[0] : {}
  // Website-Name passend setzen
  const site = websites.value.find(w => w.id === selectedWebsiteId.value)
  websiteName.value = site ? (site.name || site.url) : ''
}

async function runAudit() {
  if (!selectedWebsiteId.value) return
  auditRunning.value = true
  try {
    await api.post('/seo/run/', { website_id: selectedWebsiteId.value }) // <-- ACHTUNG: "/run/" statt nur "/"
    await fetchAudit()
  } catch {
    alert("Audit konnte nicht gestartet werden!")
  } finally {
    auditRunning.value = false
  }
}

function reloadAudit() {
  fetchAudit()
}
// Hilfsfunktionen für Ampel-Bewertung
function ampelClass(text, max, min = 0) {
  if (!text) return 'ampel rot'
  if (text.length > max) return 'ampel gelb'
  if (text.length < min) return 'ampel gelb'
  return 'ampel gruen'
}
function ampelText(text, max, min = 0) {
  if (!text) return '❌ Fehlend'
  if (text.length > max) return '🟡 Zu lang'
  if (text.length < min) return '🟡 Zu kurz'
  return '🟢 Perfekt'
}
function ampelClassNum(value, max, min = 0, invert = false) {
  if (value == null) return 'ampel rot'
  if (invert) {
    if (value > max) return 'ampel rot'
    if (value > min) return 'ampel gelb'
    return 'ampel gruen'
  } else {
    if (value > max) return 'ampel gelb'
    if (value < min) return 'ampel gelb'
    return 'ampel gruen'
  }
}
function ampelTextNum(value, max, min = 0, invert = false) {
  if (value == null) return '❌ Fehlend'
  if (invert) {
    if (value > max) return '❌ Zu langsam'
    if (value > min) return '🟡 Okay'
    return '🟢 Sehr schnell'
  } else {
    if (value > max) return '🟡 Hoch'
    if (value < min) return '🟡 Niedrig'
    return '🟢 Perfekt'
  }
}

onMounted(() => {
  fetchWebsites()
})
</script>


