// src/services/KeywordService.js
import api from '@/api/api.js';   // stellt deine axios-Instanz dar

export default {
  /**
   * Holt alle Keyword-Metriken vom Django-Backend.
   * Erwarteter Backend-Endpoint: GET /api/keywords/metrics/
   */
  getMetrics() {
    return api.get('/api/keywords/metrics/')
  }
}
