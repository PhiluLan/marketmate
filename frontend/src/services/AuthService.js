// frontend/src/services/AuthService.js
import api from "@/api/api.js";

const ACCESS_KEY  = "jwt_access_token";
const REFRESH_KEY = "jwt_refresh_token";

export function initialize() {
  const token = localStorage.getItem(ACCESS_KEY);
  if (token) {
    api.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common["Authorization"];
  }
}

export async function login(email, password) {
  delete api.defaults.headers.common["Authorization"];

  // baseURL ist jetzt /api/v1, daher nur /token/
  const res = await api.post("/token/", {
    email,
    password
  });

  const { access, refresh } = res.data;
  if (!access) throw new Error("Kein Access-Token erhalten");

  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
  api.defaults.headers.common["Authorization"] = `Bearer ${access}`;

  return res.data;
}

export async function register(email, password, role) {
  delete api.defaults.headers.common["Authorization"];
  // baseURL /api/v1 → nur /users/
  return api.post("/users/", { email, password, role });
}

export function logout() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  delete api.defaults.headers.common["Authorization"];
}

export async function getMe() {
  // holt jetzt /api/v1/users/me/
  return api.get("/users/me/");
}

export default api;
