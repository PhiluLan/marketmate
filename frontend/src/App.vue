<template>
  <div id="app">
    <nav class="main-nav">
      <router-link class="nav-link" to="/">Dashboard</router-link>
      <router-link class="nav-link" to="/scheduler">Scheduler</router-link>
      <router-link to="/manage-contents" class="nav-link">Inhalte</router-link>
      <router-link class="nav-link" to="/chat">Chat mit Lenny</router-link>
      <router-link class="nav-link" to="/integrations">Meta Ads verbinden</router-link>
      <router-link class="nav-link" to="/ads-overview">Ads Übersicht</router-link>
      <router-link class="nav-link" to="/content-calendar">Kalender</router-link>
      <router-link class="nav-link" to="/assets">Assets</router-link>
      <router-link class="nav-link" to="/personas">Personas</router-link>
      <router-link class="nav-link" to="/journey">Journey</router-link>
      <router-link class="nav-link" to="/journey-builder">Journey Builder</router-link>
      <router-link class="nav-link" to="/generate">Content-Generator</router-link>
      <router-link class="nav-link" to="/editor">SEO-Editor</router-link>
      <router-link class="nav-link" to="/assets">Asset-Generator</router-link>
      <router-link class="nav-link" to="/websites/add">Website hinzufügen</router-link>
      <router-link class="nav-link" to="/keyword-ideas">Keyword-Analyse</router-link>
      <router-link class="nav-link" to="/competitor-analysis">Konkurrenzanalyse</router-link>
      <router-link class="nav-link" to="/seo-generator">KI-Empfehlung</router-link>
      <router-link class="nav-link" to="/seo-audits">SEO-Audits</router-link>
      <router-link class="nav-link" to="/keywords">Keywords</router-link>
      <router-link class="nav-link" to="/todos">ToDos</router-link>
      <router-link v-if="!isLoggedIn" class="nav-link" to="/login">Login</router-link>
      <router-link v-if="!isLoggedIn" class="nav-link" to="/register">Register</router-link>
      <button v-if="isLoggedIn" @click="doLogout" class="nav-link text-red-600">Logout</button>
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

<style scoped src="@/assets/Navigation.css">


</style>

