<template>
  <div class="container mt-5">
    <h2 class="text-center">Inicio de Sesión</h2>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label for="username" class="form-label">Usuario</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="username"
          placeholder="Ingresa tu usuario"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          placeholder="Ingresa tu contraseña"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary w-100 mb-3">
        Iniciar Sesión
      </button>
    </form>
    <p class="text-center">
      ¿No tienes cuenta?
      <router-link to="/register" class="text-primary fw-bold">
        Regístrate aquí
      </router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
  async login() {
    try {
      const apiUrl = this.$apiUrl || "http://127.0.0.1:5000";

      const response = await fetch(`${apiUrl}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });

      if (!response.ok) {
        throw new Error("No se pudo iniciar sesión. Verifique las credenciales.");
      }

      const data = await response.json();
      if (data.token) {
        localStorage.setItem("sessionToken", data.token);
        console.log("Inicio de sesión exitoso. Token:", data.token);

        // Emitir evento global para actualizar la autenticación
        this.$authEvent.emit("auth-update", true);

        this.$router.push("/users");
      } else {
        alert(data.error || "Error desconocido");
      }
    } catch (error) {
      console.error("Error al iniciar sesión:", error.message);
      alert("No se pudo iniciar sesión. Por favor, inténtelo más tarde.");
    }
  },

  },
};
</script>

<style scoped>
.container {
  max-width: 400px;
  margin: auto;
}
</style>
