<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">Autenticador</router-link>
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
          <ul class="navbar-nav ms-auto">
            <!-- Botones para usuarios no autenticados -->
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link text-white" to="/login">Iniciar Sesión</router-link>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link class="nav-link text-white" to="/generate-token">Generar Token</router-link>
            </li>
  
            <!-- Botones para usuarios autenticados -->
            <li class="nav-item" v-if="isAuthenticated">
              <router-link class="nav-link text-white" to="/users">Usuarios</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <a class="nav-link text-white" href="#" @click="logout">Cerrar Sesión</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isAuthenticated: false, // Estado de autenticación inicial
      };
    },
    methods: {
      async validateToken() {
        const token = localStorage.getItem("sessionToken");
        if (!token) {
          this.isAuthenticated = false;
          return;
        }
  
        try {
          const apiUrl = process.env.VUE_APP_API_URL || "http://127.0.0.1:5000";
          const response = await fetch(`${apiUrl}/validate-token`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-Session-Token": token,
            },
          });
  
          if (response.ok) {
            this.isAuthenticated = true; // Token válido
          } else {
            localStorage.removeItem("sessionToken"); // Eliminar token no válido
            this.isAuthenticated = false;
          }
        } catch (error) {
          console.error("Error al validar el token:", error);
          localStorage.removeItem("sessionToken"); // Eliminar token en caso de error
          this.isAuthenticated = false;
        }
      },
      logout() {
        localStorage.removeItem("sessionToken"); // Eliminar token al cerrar sesión
        this.isAuthenticated = false;
        this.$authEvent.emit("auth-update", false); // Emitir evento de actualización
        this.$router.push("/login"); // Redirigir al login
      },
    },
    mounted() {
      this.validateToken(); // Validar token al cargar el componente
  
      // Escuchar eventos de autenticación
      this.$authEvent.on("auth-update", (status) => {
        this.isAuthenticated = status; // Actualizar estado de autenticación
      });
    },
  };
  </script>
  
  <style scoped>
  .navbar {
    margin-bottom: 20px;
  }
  </style>
  