// src/services/schedulerService.js
import api from '@/api/api'

// Wenn deine api-Instance bereits baseURL: '/api/v1' hat, brauchst du nur die Routen:
export function fetchContents() {
  return api.get('/contents/')
}

export function fetchScheduledPosts() {
  return api.get('/scheduler/')
}

export function createScheduledPost(payload) {
  return api.post('/scheduler/', payload)
}
