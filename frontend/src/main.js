// frontend/src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initialize } from "@/services/AuthService.js";
import "@/assets/tailwind.css";
import "@/assets/custom.css";

const app = createApp(App);

// 1) Token aus localStorage laden und in Axios-Defaults setzen:
initialize();

app.use(router);
app.mount("#app");
