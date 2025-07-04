<template>
  <div class="chart-wrapper">
    <h2>{{ title }}</h2>
    <canvas ref="chartCanvas" id="metric-chart"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { Chart } from 'chart.js/auto'
import api from '@/api/api.js'  // <- zentrale Axios-Instanz einbinden

const props = defineProps({
  title: String,
  type: String,
  from: String,
  to: String
})

const chartCanvas = ref(null)
let chartInstance = null

const fetchDataAndRenderChart = async () => {
  try {
    const { data } = await api.get('dashboard/metrics/', {
      params: {
        type: props.type,
        from: props.from,
        to: props.to
      }
    })

    if (!Array.isArray(data)) {
      console.error('Unerwartete API-Antwort:', data)
      return
    }

    const labels = data.map(item => item.date)
    const values = data.map(item => item.value)

    if (chartInstance) {
      chartInstance.destroy()
    }

    chartInstance = new Chart(chartCanvas.value, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: props.title,
          data: values,
          fill: false,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false
      }
    })
  } catch (err) {
    console.error('Fehler fetchDataAndRenderChart', err.response?.status, err.response?.data)
  }
}

onMounted(fetchDataAndRenderChart)
watch(() => [props.from, props.to, props.type], fetchDataAndRenderChart)
</script>


<style scoped>
.chart-wrapper {
  background: #f9f9f9;
  border: 1px solid #ccc;
  padding: 16px;
  margin-bottom: 24px;
  border-radius: 12px;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  height: 350px;
  overflow: hidden;
}

canvas {
  display: block;
  max-height: 300px;
  width: 100%;
}
</style>
