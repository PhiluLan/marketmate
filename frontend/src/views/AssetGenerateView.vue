<template>
  <div class="p-4">
    <h1 class="text-2xl mb-4">Asset-Generator</h1>

    <form @submit.prevent="onGenerate" class="space-y-4">
      <div>
        <label>Prompt:</label>
        <input type="text" v-model="prompt" class="border p-1 w-full" placeholder="z.B. sonniger Strand bei Sonnenuntergang" required />
      </div>

      <div class="flex space-x-4">
        <div>
          <label>Anzahl (1–4):</label>
          <input type="number" v-model.number="n" min="1" max="4" class="border p-1 w-16" />
        </div>
        <div>
          <label>Größe:</label>
          <select v-model="size">
            <option value="256x256">256×256</option>
            <option value="512x512">512×512</option>
            <option value="1024x1024">1024×1024</option>
          </select>
        </div>
      </div>

      <button type="submit" class="btn">Bild generieren</button>
    </form>

    <div v-if="images.length" class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div v-for="(url, idx) in images" :key="idx" class="border p-2">
        <img :src="url" alt="Generiertes Asset" class="w-full h-auto rounded" />
        <a :href="url" target="_blank" download class="block text-center mt-2 btn-secondary">
          Download
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import AssetService from '@/services/AssetService';

export default {
  name: 'AssetGenerateView',
  data() {
    return {
      prompt: '',
      n: 1,
      size: '512x512',
      images: []
    };
  },
  methods: {
    async onGenerate() {
      try {
        this.images = [];
        this.images = await AssetService.generateAssets({
          prompt: this.prompt,
          n: this.n,
          size: this.size
        });
      } catch (e) {
        console.error(e);
        alert('Fehler bei der Bilderzeugung.');
      }
    }
  }
};
</script>

<style scoped>
.btn {
  background-color: #2b6cb0; color: white; padding: 0.5rem 1rem; border: none; border-radius: .25rem;
}
.btn-secondary {
  background-color: #4a5568; color: white; padding: 0.4rem .8rem; border: none; border-radius: .25rem;
}
</style>
