import axios from 'axios'

// Keys für LocalStorage
const ACCESS_KEY  = 'jwt_access_token'
const REFRESH_KEY = 'jwt_refresh_token'

// Pfade, bei denen wir kein Token-Refresh durchführen wollen
const SKIP_REFRESH_PATHS = [
  '/users/verify-email'
]

// Basis-URL aus der Env, default /api
const BASE = import.meta.env.VITE_API_BASE_URL || '/api'

// Hilfsfunktion zum Ausloggen (Tokens löschen)
function logout() {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
  delete api.defaults.headers.common['Authorization']
}

// Axios-Instanz
const api = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true,
})

// Setze vorhandenes Access-Token initial
const initialToken = localStorage.getItem(ACCESS_KEY)
if (initialToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${initialToken}`
}

// Response-Interceptor mit Refresh-Logik
api.interceptors.response.use(
  response => response,
  async error => {
    const { config, response } = error

    // Nur bei 401 und wenn wir nicht gerade /verify-email anfragen:
    if (
      response?.status === 401 &&
      !SKIP_REFRESH_PATHS.some(path => config.url.includes(path))
    ) {
      const refreshToken = localStorage.getItem(REFRESH_KEY)
      if (refreshToken) {
        try {
          // Token erneuern
          const res = await axios.post(
            `${BASE}/token/refresh/`,
            { refresh: refreshToken },
            { headers: { 'Content-Type': 'application/json' } }
          )
          const { access, refresh } = res.data
          // Neue Tokens speichern
          localStorage.setItem(ACCESS_KEY, access)
          localStorage.setItem(REFRESH_KEY, refresh)
          // Header updaten
          api.defaults.headers.common['Authorization'] = `Bearer ${access}`
          config.headers['Authorization'] = `Bearer ${access}`
          // Original-Request erneut senden
          return api(config)
        } catch (refreshError) {
          // Refresh fehlgeschlagen → ausloggen
          logout()
          return Promise.reject(refreshError)
        }
      }
    }

    // Ansonsten Fehler normal weiterreichen
    return Promise.reject(error)
  }
)

export default api
