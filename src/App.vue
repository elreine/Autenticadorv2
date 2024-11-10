<template>
  <div id="app">
    <button @click="view = 'register'">Registro</button>
    <button @click="view = 'users'">Usuarios Registrados</button>

    <UserRegister v-if="view === 'register'" />
    <UserList v-else />
  </div>
</template>

<script>
import UserRegister from './components/UserRegister.vue';
import UserList from './components/UserList.vue';

export default {
  data() {
    return {
      view: 'register' // Controla qué vista se muestra
    };
  },
  components: {
    UserRegister,
    UserList
  }
};
</script>

<style>
#app {
  text-align: center;
}
button {
  margin: 5px;
  padding: 10px;
  font-size: 16px;
}
</style>
