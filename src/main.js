// main.js (ajustado para consistencia en la URL de la API)
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import mitt from "mitt";

// Crear EventBus para autenticación
const authEventBus = mitt();

// Validar si las variables de entorno están definidas
if (!process.env.VUE_APP_API_LOCAL || !process.env.VUE_APP_API_PRODUCTION) {
  console.error("Las variables de entorno VUE_APP_API_LOCAL o VUE_APP_API_PRODUCTION no están definidas.");
}

// Configurar la URL de la API dinámica según el entorno
const apiUrl =
  process.env.NODE_ENV === "production"
    ? process.env.VUE_APP_API_PRODUCTION
    : process.env.VUE_APP_API_LOCAL;

if (!apiUrl) {
  console.error("Error: `apiUrl` no está definido.");
}

// Log de la URL seleccionada para depuración
console.log("API URL seleccionada:", apiUrl);

// Crear la aplicación Vue
const app = createApp(App);

// Inyectar URL de la API y EventBus como propiedades globales
app.config.globalProperties.$apiUrl = apiUrl;
app.config.globalProperties.$authEvent = authEventBus;

// Usar el router
app.use(router);

// Montar la aplicación
app.mount("#app");
