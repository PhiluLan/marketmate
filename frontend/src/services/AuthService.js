// frontend/src/services/AuthService.js
import api from "@/api/api.js";

const ACCESS_KEY  = "jwt_access_token";
const REFRESH_KEY = "jwt_refresh_token";

/**
 * Initialisiert das Axios-Instance mit dem gespeicherten Access-Token (falls vorhanden).
 */
export function initialize() {
  const token = localStorage.getItem(ACCESS_KEY);
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

/**
 * Loggt den User ein, speichert die JWT-Tokens in localStorage
 * und setzt den Authorization-Header.
 */
export async function login(email, password) {
  // Entferne ggf. alten Header
  delete api.defaults.headers.common["Authorization"];

  const res = await api.post("/token/", { email, password });
  const { access, refresh } = res.data;
  if (!access) throw new Error("Kein Access-Token erhalten");

  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
  api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

  return res.data;
}

/**
 * Registriert einen neuen User.
 * Erwartet userData-Objekt mit allen benötigten Feldern:
 * {
 *   email,
 *   password,
 *   role,
 *   website_url,
 *   company_name,
 *   industry,
 *   instagram_url,
 *   facebook_url,
 *   linkedin_url
 * }
 */
export async function register(userData) {
  // Entferne alten Authorization-Header
  delete api.defaults.headers.common["Authorization"];

  const res = await api.post("/users/", userData);
  return res.data;
}

/**
 * Loggt den User aus, indem Tokens entfernt und Header gelöscht werden.
 */
export function logout() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  delete api.defaults.headers.common["Authorization"];
}

/**
 * Holt das Profil des aktuell eingeloggten Users.
 */
export async function getMe() {
  return api.get("/users/me/");
}

export default api;
