<template>
  <div class="goal-box">
    <h2 class="text-lg font-bold mb-2">🎯 Fortschritt auf dein Ziel</h2>

    <div v-if="loading">Ziel wird geladen …</div>
    <div v-else-if="!goals.realistisch">Keine Vorschläge verfügbar.</div>
    <div v-else>
      <div class="mb-2">Aktueller Stand: {{ actual.toLocaleString('de-CH') }}</div>

      <div v-for="(value, label) in goals" :key="label" class="mb-4">
        <strong>{{ label[0].toUpperCase() + label.slice(1) }}:</strong>
        <div class="bar-container">
          <div class="bar-fill" :style="{ width: getPct(value) + '%' }"></div>
        </div>
        <small>{{ getPct(value) }} % von {{ value.toLocaleString('de-CH') }}</small>
      </div>
    </div>
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

const goals = ref({})
const actual = ref(0)
const loading = ref(true)

const getPct = (target) => Math.min(100, Math.round((actual.value / target) * 100))

const loadGoals = async () => {
  loading.value = true
  try {
    const { data } = await api.get('dashboard/metrics/goals/', {
      params: { from: props.from, to: props.to, type: props.type }
    })
    goals.value = data.goals
    actual.value = data.actual
  } catch (e) {
    goals.value = {}
    actual.value = 0
  } finally {
    loading.value = false
  }
}

watch(() => [props.from, props.to, props.type], loadGoals, { immediate: true })
</script>

<style scoped>
.goal-box {
  background: #f0f8ff;
  border: 1px solid #cce;
  padding: 1rem;
  border-radius: 10px;
  max-width: 700px;
  margin: 2rem auto;
}
.bar-container {
  background: #eee;
  height: 16px;
  border-radius: 8px;
  overflow: hidden;
}
.bar-fill {
  background: #3b82f6;
  height: 100%;
  transition: width 0.3s ease;
}
</style>
