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
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">
        Iniciar Sesión
      </button>
    </form>
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
    login() {
  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: this.username,
      password: this.password,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.token) {
        localStorage.setItem("sessionToken", data.token);
        alert("Inicio de sesión exitoso");
        this.$router.push("/users");
      } else if (data.error) {
        alert(data.error);
      }
    })
    .catch((error) => {
      console.error("Error al iniciar sesión:", error.message);
      alert("Hubo un problema al iniciar sesión. Verifica tus credenciales.");
    });
}

  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
}
</style>
