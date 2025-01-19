<template>
  <div class="container mt-5">
    <h2 class="text-center">Bienvenido, {{ username }}</h2>
    <p class="text-center">Estamos encantados de verte aquí.</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "", // Nombre del usuario
    };
  },
  mounted() {
    // Obtener el nombre del usuario desde el token almacenado
    const token = localStorage.getItem("sessionToken");
    if (token) {
      try {
        // Decodificar token (ejemplo usando formato JWT)
        const payload = JSON.parse(atob(token.split(".")[1]));
        this.username = payload.username || "Usuario";
      } catch (error) {
        console.error("Error al decodificar el token:", error);
        this.username = "Usuario";
      }
    }
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
}
</style>
