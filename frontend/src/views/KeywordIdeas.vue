<template>
  <div class="ideas-container">
    <h2>Keyword-Analyse</h2>

    <div class="form-group">
      <input
        v-model="term"
        @keyup.enter="fetchIdeas"
        placeholder="Suchbegriff eingeben"
      />
      <select v-model="region">
        <option value="">— Region wählen —</option>
        <option value="CH">Schweiz (CH)</option>
        <option value="DE">Deutschland (DE)</option>
        <option value="AT">Österreich (AT)</option>
      </select>
      <button @click="fetchIdeas">Analyse starten</button>
    </div>

    <div v-if="loading" class="loading">Lade…</div>
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 1) Seed -->
    <div v-if="seedIdea" class="seed-section">
      <h3>Eingegebenes Keyword</h3>
      <div class="idea-card">
        <p><strong>Keyword:</strong> {{ seedIdea.keyword }}</p>
        <p><strong>Region:</strong> {{ seedIdea.region || '–' }}</p>
        <p><strong>Suchvolumen:</strong> {{ seedIdea.monthly_searches }}</p>
        <p><strong>Wettbewerb:</strong> {{ seedIdea.competition }}</p>
        <p>
          <strong>CPC:</strong>
          {{ seedIdea.low_cpc.toFixed(2) }} € – {{ seedIdea.high_cpc.toFixed(2) }} €
        </p>
      </div>
    </div>

    <!-- Trennlinie -->
    <hr v-if="suggestionIdeas.length" class="separator" />

    <!-- 2) Vorschläge -->
    <div v-if="suggestionIdeas.length" class="suggestions-section">
      <h3>Vorschläge (max. 20)</h3>
      <div class="ideas-list">
        <div
          class="idea-card"
          v-for="idea in suggestionIdeas"
          :key="idea.keyword"
        >
          <p><strong>Keyword:</strong> {{ idea.keyword }}</p>
          <p><strong>Suchvolumen:</strong> {{ idea.monthly_searches }}</p>
          <p><strong>Wettbewerb:</strong> {{ idea.competition }}</p>
          <p>
            <strong>CPC:</strong>
            {{ idea.low_cpc.toFixed(2) }} € – {{ idea.high_cpc.toFixed(2) }} €
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'KeywordIdeas',
  data() {
    return {
      term: '',
      region: '',
      ideas: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    // sucht das Seed-Keyword
    seedIdea() {
      return this.ideas.find(
        (i) => i.keyword.toLowerCase() === this.term.toLowerCase()
      );
    },
    // alles außer Seed
    suggestionIdeas() {
      return this.ideas.filter(
        (i) => i.keyword.toLowerCase() !== this.term.toLowerCase()
      );
    },
  },
  methods: {
    async fetchIdeas() {
      if (!this.term) {
        this.error = 'Bitte erst ein Keyword eingeben.';
        return;
      }
      this.loading = true;
      this.error = null;
      this.ideas = [];
      try {
        const res = await axios.get('/api/keywords/ideas/', {
          params: { term: this.term, region: this.region }
        });
        this.ideas = res.data;
      } catch (err) {
        this.error =
          err.response?.data?.error ||
          err.response?.data?.detail ||
          'Fehler beim Laden.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.ideas-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}
.form-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.form-group input,
.form-group select {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.form-group button {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #007bff;
  color: white;
}
.form-group button:hover {
  background: #0056b3;
}

.loading {
  font-style: italic;
}
.error {
  color: #c00;
  margin-bottom: 1rem;
}

/* Seed-Section */
.seed-section {
  margin-bottom: 2rem;
  padding: 1rem;
  border: 2px solid #007bff;
  border-radius: 4px;
  background: #f0f8ff;
}
.separator {
  border: none;
  border-top: 2px dashed #007bff;
  margin: 2rem 0;
}

/* Vorschläge */
.suggestions-section h3 {
  margin-bottom: 1rem;
}
.ideas-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}
.idea-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 0.75rem;
  background: #fafafa;
}
.idea-card h3 {
  margin-top: 0;
}
.idea-card p {
  margin: 0.25rem 0;
  font-size: 0.95rem;
}
</style>
