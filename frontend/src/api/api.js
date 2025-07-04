// frontend/src/api/api.js
import axios from 'axios'

// 1) Hol dir die URL aus den Vite-Env-Variablen
const BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'


export const api = axios.create({
  // 2) Vollständiger Pfad auf Django-API root + version
  baseURL: `${BASE}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

// 3) JWT-Token (falls du ihn schon im localStorage hast)
const token = localStorage.getItem('jwt_access_token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export default api
