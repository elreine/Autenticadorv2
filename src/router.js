import { createRouter, createWebHistory } from 'vue-router';
import UserRegister from './components/UserRegister.vue';
import UserLogin from './components/UserLogin.vue'; // Cambiado a UserLogin
import UserList from './components/UserList.vue';
import GenerateToken from './components/GenerateToken.vue';

const routes = [
  {
    path: '/register',
    name: 'Register',
    component: UserRegister,
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin, // Cambiado a UserLogin
  },
  {
    path: '/users',
    name: 'Users',
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
