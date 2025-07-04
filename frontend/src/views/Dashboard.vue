<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Marketing-Cockpit</h1>

    <!-- Filterbereich -->
    <div class="mb-6 flex flex-wrap items-center gap-4">
      <label>
        Von: <input type="date" v-model="from" class="border px-2 py-1 rounded" />
      </label>
      <label>
        Bis: <input type="date" v-model="to" class="border px-2 py-1 rounded" />
      </label>
    </div>

    <!-- KPI-Kacheln -->
    <div class="flex flex-wrap gap-4 mb-6">
      <DashboardKpiCard
        v-for="kpi in kpis"
        :key="kpi.type"
        :title="titles[kpi.type]"
        :value="kpi.value"
        :change="kpi.change_pct"
      />
    </div>

    <GoalProgress :from="from" :to="to" type="organic_sessions" />


    <GoalSuggestion :from="from" :to="to" type="organic_sessions" />

    <!-- Diagramme -->
    <DashboardMetricChart title="Organische Sessions" type="organic_sessions" :from="from" :to="to" />
    <DashboardMetricChart title="Conversions" type="conversions" :from="from" :to="to" />
    <DashboardMetricChart title="Ad Spend" type="ad_spend" :from="from" :to="to" />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import DashboardMetricChart from './DashboardMetricChart.vue'
import DashboardKpiCard from './DashboardKpiCard.vue'
import api from '@/api/api.js'
import GoalSuggestion from './GoalSuggestion.vue'
import GoalProgress from './GoalProgress.vue'



const today = new Date()
const lastMonth = new Date()
lastMonth.setDate(today.getDate() - 30)

const formatDate = (date) => date.toISOString().split('T')[0]

const from = ref(formatDate(lastMonth))
const to = ref(formatDate(today))

const kpis = ref([])
const titles = {
  organic_sessions: 'Organische Sessions',
  conversions: 'Conversions',
  ad_spend: 'Ad Spend'
}

const fetchKpis = async () => {
  try {
    const { data } = await api.get('dashboard/metrics/summary/', {
      params: { from: from.value, to: to.value }
    })
    kpis.value = data
  } catch (err) {
    console.error('Fehler beim Laden der KPI-Summary', err)
  }
}

watch([from, to], fetchKpis, { immediate: true })
</script>
