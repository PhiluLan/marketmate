<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Content-Generator</h1>

    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <label>Format</label>
        <select v-model="form.type" required>
          <option value="blog">Blog</option>
          <option value="social">Social Media</option>
          <option value="email">E-Mail</option>
        </select>
      </div>

      <div>
        <label>Ton</label>
        <select v-model="form.tone" required>
          <option value="seriös">Seriös</option>
          <option value="locker">Locker</option>
          <option value="technisch">Technisch</option>
        </select>
      </div>

      <div>
        <label>Länge</label>
        <select v-model="form.length" required>
          <option value="short">Kurz</option>
          <option value="medium">Mittel</option>
          <option value="long">Lang</option>
        </select>
      </div>

      <div>
        <label>Thema</label>
        <input
          type="text"
          v-model="form.topic"
          placeholder="z.B. Sommer Cocktails"
          required
          class="border p-1 w-full"
        />
      </div>

      <button type="submit" class="btn">Generieren</button>
    </form>

    <div v-if="result" class="mt-6">
      <h2 class="font-semibold mb-2">Ergebnis</h2>
      <pre class="bg-gray-100 p-3 rounded whitespace-pre-wrap">{{ result }}</pre>
      <button @click="copy" class="btn-secondary mt-2">
        In Zwischenablage kopieren
      </button>
    </div>
  </div>
</template>

<script>
import ContentService from '@/services/ContentService';

export default {
  name: 'ContentGenerateView',
  data() {
    return {
      form: {
        type: 'blog',
        tone: 'locker',
        length: 'medium',
        topic: ''
      },
      result: ''
    };
  },
  methods: {
    async onSubmit() {
      try {
        this.result = ''; // Clear vorheriges Ergebnis
        this.result = await ContentService.generateContent(this.form);
      } catch (err) {
        console.error(err);
        alert('Fehler beim Generieren');
      }
    },
    copy() {
      navigator.clipboard.writeText(this.result)
        .then(() => alert('Kopiert!'))
        .catch(() => alert('Kopieren fehlgeschlagen'));
    }
  }
};
</script>

<style scoped>
.btn {
  background-color: #2b6cb0; /* Beispiel-Farbe */
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
}
.btn-secondary {
  background-color: #4a5568;
  color: white;
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 0.25rem;
}
</style>
