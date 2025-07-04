// frontend/src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initialize } from "@/services/AuthService.js";
import "@/assets/tailwind.css";
import "@/assets/custom.css";

// 1) Token aus localStorage laden und in Axios-Defaults setzen:
initialize();

const app = createApp(App);

app.use(router);
app.mount("#app");
