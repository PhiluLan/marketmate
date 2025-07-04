<template>
  <div class="p-6">
    <h2 class="text-xl mb-4">Meta Ads Integration</h2>
    <button
      v-if="!connected"
      @click="connect()"
      class="btn-blue">
      Mit Meta Ads verbinden
    </button>
    <p v-else class="text-green-600">
      Verbunden! <router-link to="/ads-overview">Zur Übersicht</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data(){ return { connected: false } },
  async mounted(){
    try {
      // Ping Overview, wenn 200 → verbunden
      await this.$axios.get('/api/v1/integrations/meta/overview/')
      this.connected = true
    } catch { this.connected = false }
  },
  methods:{
    connect(){ window.location = '/api/v1/integrations/meta/connect/' }
  }
}
</script>
