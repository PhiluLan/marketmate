<template>
  <div class="kpi-card">
    <div class="label">{{ title }}</div>
    <div class="value">{{ formattedValue }}</div>
    <div :class="changeClass">{{ signedChange }}%</div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  value: Number,
  change: Number
})

const formattedValue = props.value.toLocaleString('de-CH')
const signedChange = props.change > 0 ? `+${props.change}` : `${props.change}`
const changeClass = props.change >= 0 ? 'change up' : 'change down'
</script>

<style scoped>
.kpi-card {
  background: #f9f9f9;
  border: 1px solid #ddd;
  padding: 1rem;
  border-radius: 8px;
  width: 200px;
  text-align: center;
}
.label {
  font-size: 0.9rem;
  color: #666;
}
.value {
  font-size: 1.4rem;
  font-weight: bold;
}
.change.up {
  color: green;
}
.change.down {
  color: red;
}
</style>
