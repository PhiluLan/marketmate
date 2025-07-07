<template>
  <div id="app">
    <nav class="main-nav">
      <router-link to="/" class="logo">MarketMate</router-link>
      <div class="menu-wrapper" @mouseleave="menuOpen = false">
        <button class="menu-button" @click="toggleMenu">
          Menü
          <span :class="['arrow', menuOpen ? 'open' : '']"></span>
        </button>
        <div v-show="menuOpen" class="dropdown-menu">
          <!-- Spalte 1 -->
          <div class="dropdown-col">
            <router-link to="/" class="dropdown-link">Home</router-link>
            <router-link to="/dashboard" class="dropdown-link">Dashboard</router-link>
            <router-link to="/integrations/google" class="dropdown-link">Google Ads</router-link>
            <router-link to="/scheduler" class="dropdown-link">Scheduler</router-link>
            <router-link to="/manage-contents" class="dropdown-link">Inhalte</router-link>
          </div>
          <!-- Spalte 2 -->
          <div class="dropdown-col">
            <router-link to="/chat" class="dropdown-link">Chat mit Lenny</router-link>
            <router-link to="/integrations" class="dropdown-link">Meta Ads verbinden</router-link>
            <router-link to="/ads-overview" class="dropdown-link">Ads Übersicht</router-link>
            <router-link to="/content-calendar" class="dropdown-link">Kalender</router-link>
            <router-link to="/assets" class="dropdown-link">Assets</router-link>
          </div>
          <!-- Spalte 3 -->
          <div class="dropdown-col">
            <router-link to="/personas" class="dropdown-link">Personas</router-link>
            <router-link to="/journey" class="dropdown-link">Journey</router-link>
            <router-link to="/journey-builder" class="dropdown-link">Journey Builder</router-link>
            <router-link to="/generate" class="dropdown-link">Content-Generator</router-link>
            <router-link to="/editor" class="dropdown-link">SEO-Editor</router-link>
          </div>
          <!-- Spalte 4 -->
          <div class="dropdown-col">
            <router-link to="/websites/add" class="dropdown-link">Website hinzufügen</router-link>
            <router-link to="/keyword-ideas" class="dropdown-link">Keyword-Analyse</router-link>
            <router-link to="/competitor-analysis" class="dropdown-link">Konkurrenzanalyse</router-link>
            <router-link to="/seo-generator" class="dropdown-link">KI-Empfehlung</router-link>
            <router-link to="/seo-audits" class="dropdown-link">SEO-Audits</router-link>
            <router-link to="/keywords" class="dropdown-link">Keywords</router-link>
            <router-link to="/todos" class="dropdown-link">ToDos</router-link>
          </div>
        </div>
      </div>
      <div class="auth-wrapper">
        <router-link v-if="!isLoggedIn" to="/login" class="nav-link">Login</router-link>
        <router-link v-if="!isLoggedIn" to="/register" class="nav-link">Register</router-link>
        <button v-if="isLoggedIn" @click="doLogout" class="nav-link logout-button">Logout</button>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { logout } from '@/services/AuthService'

const menuOpen  = ref(false)
function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

// Auth
const isLoggedIn = computed(() => !!localStorage.getItem('jwt_access_token'))
function doLogout() {
  logout()
  window.location.reload()
}
</script>

<style scoped>
/* --- Navigation Bar --- */
.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #ffffff;
  padding: 0 20px;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: relative;
  z-index: 10;
}
.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4a90e2;
  text-decoration: none;
}
.menu-wrapper {
  position: relative;
}
.menu-button {
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  padding: 8px;
  color: #333;
}
.menu-button .arrow {
  display: inline-block;
  margin-left: 6px;
  border: solid #333;
  border-width: 0 1px 1px 0;
  padding: 3px;
  transform: rotate(45deg);
  transition: transform 0.2s;
}
.menu-button .arrow.open {
  transform: rotate(-135deg);
}

/* --- Mega Dropdown --- */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 4px;
  background: #fff;
  color: #333;
  padding: 20px;
  display: grid;
  grid-template-columns: repeat(4, auto);
  gap: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 4px;
  min-width: 600px;
}
.dropdown-col {
  display: flex;
  flex-direction: column;
}
.dropdown-link {
  margin-bottom: 8px;
  color: #333;
  text-decoration: none;
  font-size: 0.95rem;
}
.dropdown-link:hover {
  color: #4a90e2;
}

/* --- Auth Links --- */
.auth-wrapper {
  display: flex;
  align-items: center;
}
.nav-link {
  margin-left: 20px;
  font-size: 0.95rem;
  color: #333;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
}
.logout-button {
  color: #e74c3c;
}

/* --- Close dropdown when clicking outside --- */
.menu-wrapper:focus-within .dropdown-menu,
.menu-wrapper:hover .dropdown-menu {
  display: grid;
}
</style>
