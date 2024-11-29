import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './components/UserLogin.vue';
import UserRegister from './components/UserRegister.vue';
import UserList from './components/UserList.vue';
import GenerateToken from './components/GenerateToken.vue';

const routes = [
  {
    path: '/',
    redirect: '/login', // Redirigir a la página de inicio de sesión
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin,
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister,
  },
  {
    path: '/users',
    name: 'UserList',
    component: UserList,
  },
  {
    path: '/generate-token',
    name: 'GenerateToken',
    component: GenerateToken,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
