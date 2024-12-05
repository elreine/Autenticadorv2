<template>
  <div>
    <!-- Header -->
    <NavigationBar />

    <!-- Main Content -->
    <main class="container">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center text-lg-start mt-4">
      <div class="text-center p-3">
        © 2024 Autenticador - Todos los derechos reservados
      </div>
    </footer>
  </div>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";

export default {
  name: "App",
  components: {
    NavigationBar,
  },
};
</script>

<style scoped>
/* Espacio entre el header y el contenido */
main {
  margin-top: 20px;
}

/* Personalizar el footer */
footer {
  background-color: #f8f9fa;
  color: #6c757d;
}
</style>
