<template>
  <div class="p-6">
    <h2 class="text-xl mb-4">Laufende Meta Ads</h2>
    <table class="min-w-full text-left">
      <thead><tr><th>Name</th><th>Impr.</th><th>Klicks</th><th>Spend</th></tr></thead>
      <tbody>
        <tr v-for="ad in ads" :key="ad.id">
          <td>{{ ad.name }}</td>
          <td>{{ ad.insights.data[0]?.impressions }}</td>
          <td>{{ ad.insights.data[0]?.clicks }}</td>
          <td>CHF {{ ad.insights.data[0]?.spend }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data(){ return { ads: [] } },
  async mounted(){
    const { data } = await this.$axios.get('/api/v1/integrations/meta/overview/')
    this.ads = data.data || []
  }
}
</script>
