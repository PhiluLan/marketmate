<template>
  <div class="p-4">
    <h1 class="text-xl mb-4">Google Ads-Integration</h1>

    <div class="mb-6">
      <!-- Nur als verbunden zeigen, wenn wirklich eine account_id existiert -->
      <button
        v-if="!connected"
        @click="connect"
        class="bg-blue-600 text-white py-2 px-4 rounded"
      >
        Mit Google Ads verbinden
      </button>

      <p v-else class="text-green-600">
        Verbunden als Google Ads Konto: 
        <strong>{{ accountId }}</strong>
        <small class="text-gray-500">(Integration-ID {{ integration.id }})</small>
      </p>
    </div>

    <div v-if="connected">
      <h2 class="text-lg mb-2">Deine Kampagnen</h2>
      <ul>
        <li
          v-for="c in campaigns"
          :key="c.id"
          class="border p-2 rounded mb-1"
        >
          {{ c.id }} – {{ c.name }} ({{ c.status }})
        </li>
        <li v-if="campaigns.length === 0" class="italic text-gray-500">
          Keine Kampagnen gefunden.
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api from '@/api/api'

export default {
  name: 'GoogleIntegrationView',
  data() {
    return {
      integration: null,
      campaigns: []
    }
  },
  computed: {
    // Nur dann verbunden, wenn eine echte Google-Kunden-ID vorliegt
    connected() {
      return !!(this.integration && this.integration.account_id)
    },
    // Zeigt die Google Ads Kunden-ID, oder als Fallback die DB-ID
    accountId() {
      if (!this.integration) return '–'
      return this.integration.account_id 
        ? this.integration.account_id 
        : `(${this.integration.id} ohne Kunden-ID)`
    }
  },
  async created() {
    // 1) Lade Integration des eingeloggten Users
    const res = await api.get('/integrations/')
    this.integration = res.data.find(i => i.provider === 'google') || null

    // 2) Nur wenn wirklich verbunden, Kampagnen laden
    if (this.connected) {
      await this.loadCampaigns()
    }
  },
  methods: {
    async connect() {
      // Holt die OAuth-Start-URL (mit JWT im state) und leitet weiter
      const { data } = await api.get('/integrations/google/auth-url/')
      window.location.href = data.auth_url
    },
    async loadCampaigns() {
      try {
        const res = await api.get(`/integrations/${this.integration.id}/campaigns/`)
        this.campaigns = res.data
      } catch (e) {
        console.error("Fehler beim Laden der Kampagnen:", e)
        this.campaigns = []
      }
    }
  }
}
</script>
