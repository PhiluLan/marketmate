// frontend/src/api/api.js
import axios from 'axios'

// 1) Basis-URL aus der Env, default /api
const BASE = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: BASE,                         // <— jetzt nur /api
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,                 // falls Cookies benötigt werden
})

// 2) JWT-Token-Header setzen, falls vorhanden
const token = localStorage.getItem('jwt_access_token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

export default api
