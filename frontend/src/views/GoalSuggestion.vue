<template>
  <div class="goal-box">
    <h2 class="text-lg font-bold mb-2">🎯 Zielvorschlag</h2>
    <div v-if="loading">Lade Vorschlag von heyLenny …</div>
    <div v-else>{{ suggestion }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '@/api/api.js'

const props = defineProps({
  from: String,
  to: String,
  type: String
})

const loading = ref(true)
const suggestion = ref('')

const fetchSuggestion = async () => {
  loading.value = true
  try {
    const { data } = await api.get('dashboard/metrics/goals/', {
      params: {
        from: props.from,
        to: props.to,
        type: props.type
      }
    })
    suggestion.value = data.text
  } catch (err) {
    suggestion.value = 'Keine Vorschläge verfügbar.'
  } finally {
    loading.value = false
  }
}

watch(() => [props.from, props.to, props.type], fetchSuggestion, { immediate: true })
</script>

<style scoped>
.goal-box {
  background: #fff9e6;
  border: 1px solid #f0d98a;
  padding: 1rem;
  border-radius: 10px;
  max-width: 700px;
  margin: 0 auto 2rem;
}
</style>
