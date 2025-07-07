<template>
  <div class="landing-container">
    <h1>Willkommen bei MarketMate</h1>
    <p>
      Plane, verteile und optimiere all deine Kampagnen auf Social, E-Mail und Google&nbsp;Ads – alles in einem Tool.
    </p>
    <button @click="$router.push({ name: 'Dashboard' })">
      Zum Tool starten
    </button>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
}
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  text-align: center;
  /* sanfter Farbverlauf von Blau zu Lila */
  background: linear-gradient(135deg, #4a90e2 0%, #9013fe 100%);
  color: white;
}

.landing-container h1 {
  font-size: 3rem;
  margin: 0 0 20px;
}

.landing-container p {
  font-size: 1.25rem;
  margin: 0 0 30px;
  max-width: 600px;
  line-height: 1.4;
}

.landing-container button {
  background-color: white;
  color: #4a90e2;
  border: none;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.landing-container button:hover {
  background-color: #f0f0f0;
}
</style>
