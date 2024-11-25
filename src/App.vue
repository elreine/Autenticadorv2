<template>
  <div>
    <!-- Header -->
    <header>
      <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
        <div class="container">
          <a class="navbar-brand" href="#">Autenticador</a>
          <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
              <li class="nav-item">
                <router-link to="/register" class="nav-link">Registro</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/users" class="nav-link">Usuarios Registrados</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

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
export default {
  name: "App",
};
</script>

<style scoped>
/* Agregar espacio entre el header y el contenido */
main {
  margin-top: 20px;
}

/* Personalizar el footer */
footer {
  background-color: #f8f9fa;
  color: #6c757d;
}
</style>
