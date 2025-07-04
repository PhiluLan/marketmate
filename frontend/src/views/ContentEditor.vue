<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">SEO-optimierter Editor</h1>
    <textarea
      v-model="text"
      @input="analyze"
      placeholder="Schreibe hier deinen Text..."
      class="w-full h-48 border p-2 mb-4"
    ></textarea>

    <div class="space-x-4">
      <span class="badge" :class="badgeClass('flesch')">
        Flesch-Score: {{ analysis.flesch_score }}
      </span>
      <span class="badge" :class="badgeClass('density')">
        Keyword-Density: {{ analysis.keyword_density }}%
      </span>
      <span class="badge" :class="badgeClass('meta')">
        {{ analysis.meta_advice }}
      </span>
    </div>

    <div class="mt-4">
      <label>Keyword (optional):</label>
      <input
        type="text"
        v-model="keyword"
        @input="analyze"
        class="border p-1 ml-2"
        placeholder="z.B. Sommer Cocktails"
      />
    </div>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'ContentEditor',
  data() {
    return {
      text: '',
      keyword: '',
      analysis: {
        flesch_score: 0,
        keyword_density: 0,
        meta_advice: ''
      },
      timer: null
    };
  },
  methods: {
    analyze() {
      // Debounce: Warte 500ms nach letzter Eingabe
      clearTimeout(this.timer);
      this.timer = setTimeout(async () => {
        try {
          const resp = await api.post('seo/analyze/', {
            text: this.text,
            keyword: this.keyword
          });
          this.analysis = resp.data;
        } catch (e) {
          console.error('SEO-Analyse fehlgeschlagen', e);
        }
      }, 500);
    },
    badgeClass(type) {
      const val = this.analysis[
        type === 'flesch' ? 'flesch_score'
        : type === 'density' ? 'keyword_density'
        : 'meta_advice'
      ];
      // einfache Farblogik:
      if (type === 'flesch')      return val >= 60 ? 'badge-green' : 'badge-red';
      if (type === 'density')     return val >= 1 && val <= 3 ? 'badge-green' : 'badge-red';
      if (type === 'meta')        return val.includes('OK')  ? 'badge-green' : 'badge-red';
      return '';
    }
  }
};
</script>

<style scoped>
.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-weight: 500;
}
.badge-green { background-color: #48bb78; color: white; }
.badge-red   { background-color: #f56565; color: white; }
</style>
