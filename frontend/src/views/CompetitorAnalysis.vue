<template>
  <div class="competitor-analysis">
    <h1>Konkurrenzanalyse</h1>

    <form @submit.prevent="fetchCompetitorData" class="form">
      <div class="form-group">
        <label for="domain">Domain</label>
        <input id="domain" v-model="domain" placeholder="z.B. volta­braeu.ch" required />
      </div>

      <div class="form-group">
        <label for="keywords">Keywords (Komma-separiert)</label>
        <input
          id="keywords"
          v-model="keywords"
          placeholder="restaurant basel, brauerei basel"
          required
        />
      </div>

      <div class="form-group">
        <label for="region">Region (TLD, z.B. CH, DE)</label>
        <input id="region" v-model="region" placeholder="CH" />
      </div>

      <button type="submit">Analysieren</button>
    </form>

    <section v-if="results.length" class="results">
      <h2>Ergebnisse für {{ domain }}</h2>
      <table>
        <thead>
          <tr>
            <th>Keyword</th>
            <th>Position</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in results" :key="row.keyword">
            <td>{{ row.keyword }}</td>
            <td>
              <span v-if="row.position !== null">{{ row.position }}</span>
              <span v-else class="no-data">–</span>
            </td>
            <td>
              <a v-if="row.url" :href="row.url" target="_blank">{{ row.url }}</a>
              <span v-else class="no-data">nicht in Top 20</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import { ref } from 'vue'
// statt 'axios' hier deinen api-Client importieren:
import api from '@/api/api.js'

export default {
  name: 'CompetitorAnalysis',
  setup() {
    const domain = ref('')
    const keywords = ref('')
    const region = ref('CH')
    const results = ref([])
    const error = ref('')

    const fetchCompetitorData = async () => {
      error.value = ''
      results.value = []
      try {
        const resp = await api.get('/keywords/competitor/', {
          params: {
            domain: domain.value,
            keywords: keywords.value,
            region: region.value
          }
        })
        results.value = resp.data
      } catch (e) {
        if (e.response?.status === 401) {
          error.value = 'Nicht angemeldet – bitte einloggen.'
        } else {
          error.value = e.response?.data?.detail || 'Fehler bei der Anfrage'
        }
      }
    }

    return { domain, keywords, region, results, error, fetchCompetitorData }
  }
}
</script>

<style scoped>
.competitor-analysis {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  grid-column: span 2;
  padding: 0.75rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #369f6e;
}

.results table {
  width: 100%;
  border-collapse: collapse;
}

.results th, .results td {
  padding: 0.75rem;
  border: 1px solid #ddd;
  text-align: left;
}

.no-data {
  color: #999;
  font-style: italic;
}

.error {
  color: #c0392b;
  font-weight: bold;
  margin-top: 1rem;
}
</style>
