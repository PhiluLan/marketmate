// frontend/src/services/AuthService.js
import api from "@/api/api.js";

/**
 * Named Exports
 * - initialize: Token aus localStorage holen und in api.defaults.headers.common["Authorization"] setzen.
 * - login: Login-Aufruf machen, Token in localStorage ablegen und in api.defaults setzen.
 * - register: Registrierung (ohne Authorization).
 * - logout: Token entfernen.
 * - getMe: /users/me/ abrufen.
 */

export function initialize() {
  const token = localStorage.getItem("token");
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

export async function login(email, password) {
  // Vorhergehende Header entfernen (falls noch ein alter Token gesetzt war)
  delete api.defaults.headers.common["Authorization"];

  // POST /users/login/ → { access: "<JWT-Token>" } zurückerwartet
  const res = await api.post("/users/login/", { email, password });

  // Prüfen, wo der Token im Response liegt (z.B. res.data.access oder res.data.token)
  const token = res.data.access || res.data.token;
  if (!token) {
    throw new Error("Login hat keinen JWT-Token zurückgegeben.");
  }

  // 1) Token in localStorage speichern
  localStorage.setItem("token", token);
  // 2) Header in Axios-Defaults setzen
  api.defaults.headers.common["Authorization"] = `Bearer ${token}`;

  return res.data;
}

export async function register(email, password, role) {
  // Vorherigen Authorization-Header entfernen (Registration braucht keinen Token)
  delete api.defaults.headers.common["Authorization"];
  return api.post("/users/", { email, password, role });
}

export function logout() {
  localStorage.removeItem("token");
  delete api.defaults.headers.common["Authorization"];
}

export async function getMe() {
  return api.get("/users/me/");
}

/**
 * Default Export: Einfach das api-Objekt selbst, falls mal direkt verwendet.
 * (Nicht zwingend erforderlich, aber kann nützlich sein.)
 */
export default api;
