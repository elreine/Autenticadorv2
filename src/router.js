import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "./components/UserLogin.vue";
import UserRegister from "./components/UserRegister.vue";
import UserList from "./components/UserList.vue";
import GenerateToken from "./components/GenerateToken.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "Login", component: UserLogin },
  { path: "/register", name: "Register", component: UserRegister },
  {
    path: "/generate-token",
    name: "GenerateToken",
    component: GenerateToken,
    meta: { requiresGuest: true },
  },
  {
    path: "/users",
    name: "Users",
    component: UserList,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Guardas de navegación
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("sessionToken");

  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirigir a login si la ruta requiere autenticación y no hay token
    next("/login");
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // Redirigir a usuarios si la ruta es para invitados y hay un token válido
    next("/users");
  } else {
    next();
  }
});

export default router;
