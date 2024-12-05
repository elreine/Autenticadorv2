import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import mitt from 'mitt'; // Importa mitt

const authEventBus = mitt(); // Crea el EventBus

const app = createApp(App);

// Inyecta el EventBus como una propiedad global
app.config.globalProperties.$authEvent = authEventBus;

app.use(router).mount("#app");

console.log("API URL:", process.env.VUE_APP_API_URL); // Verifica que se cargue la URL correctamente
