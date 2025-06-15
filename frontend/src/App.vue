<template>
  <div id="app">
    <nav style="background:#f0f0f0; padding:1rem; display:flex; gap:1rem;">
      <router-link to="/">Dashboard</router-link>
      <router-link to="/websites/add">Website hinzufügen</router-link>
      <router-link to="/keyword-ideas">Keyword-Analyse</router-link>
      <router-link to="/competitor-analysis">Konkurrenzanalyse</router-link>
      <router-link to="/seo-generator">KI-Empfehlung</router-link>
      <router-link to="/seo-audits">SEO-Audits</router-link>
      <router-link to="/keywords">Keywords</router-link>
      <router-link to="/todos" class="hover:underline">ToDos</router-link>
      <router-link v-if="!isLoggedIn" to="/login">Login</router-link>
      <router-link v-if="!isLoggedIn" to="/register">Register</router-link>
      <button v-if="isLoggedIn" @click="doLogout">Logout</button>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { logout } from '@/services/AuthService'

const isLoggedIn = computed(() => !!localStorage.getItem('token'))

function doLogout() {
  logout()
  window.location.reload()
}
</script>
