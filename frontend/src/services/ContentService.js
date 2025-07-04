// src/services/ContentService.js
import api from '@/api/api.js';  // dein Axios-Wrapper
const BASE = '/contents'

export default {
  /**
   * Ruft die Backend-Route zum Generieren von Content auf.
   * @param {{type:string, tone:string, length:string, topic:string}} payload
   * @returns {Promise<string>} generierter Text
   */
  generateContent(payload) {
    // Dein baseURL ist vermutlich schon auf /api/v1/ gesetzt
    return api
      .post('content/generate/', payload)
      .then(response => response.data.content);
  }
};

export function fetchContents() {
  return api.get(BASE + '/')
}
export function createContent(payload) {
  return api.post(BASE + '/', payload)
}
