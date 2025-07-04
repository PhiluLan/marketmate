<template>
  <div class="p-4">
    <h1 class="text-xl mb-4">Inhalte verwalten</h1>

    <form @submit.prevent="onCreate" class="mb-6 space-y-2">
      <input v-model="form.title" placeholder="Titel" required class="border p-2 w-full"/>
      <textarea v-model="form.body" placeholder="Text" class="border p-2 w-full"/>
      <!-- Ads-Felder optional -->
      <input v-model="form.ad_account_id" placeholder="Ad Account ID" class="border p-2 w-full"/>
      <input v-model.number="form.daily_budget" type="number" placeholder="Budget (Cent)" class="border p-2 w-full"/>
      <button type="submit" class="bg-green-500 text-white py-2 px-4 rounded">Speichern</button>
    </form>

    <ul>
      <li v-for="c in contents" :key="c.id" class="border p-2 rounded mb-2">
        {{ c.id }} – {{ c.title }}
      </li>
    </ul>
  </div>
</template>

<script>
import { fetchContents, createContent } from '@/services/ContentService.js'

export default {
  name: 'ContentManageView',
  data() {
    return {
      contents: [],
      form: {
        title: '',
        body: '',
        ad_account_id: '',
        daily_budget: null
      }
    }
  },
  async created() {
    this.load()
  },
  methods: {
    async load() {
      this.contents = (await fetchContents()).data
    },
    async onCreate() {
      await createContent(this.form)
      this.form = { title:'', body:'', ad_account_id:'', daily_budget:null }
      this.load()
    }
  }
}
</script>
