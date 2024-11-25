import { createRouter, createWebHistory } from "vue-router";
import UserRegister from "./components/UserRegister.vue";
import UserList from "./components/UserList.vue";
import GenerateToken from "./components/GenerateToken.vue";

const routes = [
  { path: "/", component: UserRegister },
  { path: "/users", component: UserList },
  { path: "/generate-token", component: GenerateToken }, // Nueva ruta
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
