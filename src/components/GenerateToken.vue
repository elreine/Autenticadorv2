<template>
  <div class="container mt-5">
    <h2 class="text-center">Generar Token</h2>
    <p class="text-center">Este token es necesario para registrarse.</p>
    <button class="btn btn-primary w-100" @click="generateToken">
      Generar Token
    </button>
    <div v-if="token" class="mt-3 alert alert-success">
      <h4 class="text-center">Tu Token:</h4>
      <code class="d-block bg-light p-2 text-center">{{ token }}</code>
    </div>
    <div v-if="error" class="mt-3 alert alert-danger">
      <h4 class="text-center">Error:</h4>
      <p class="text-center">{{ error }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      token: null, // Token generado
      error: null, // Mensaje de error
    };
  },
  methods: {
    async generateToken() {
      const apiUrl = process.env.VUE_APP_API_URL || "http://127.0.0.1:5000"; // Valor por defecto
      console.log("API URL utilizada:", apiUrl); // Depuración

      try {
        const response = await fetch(`${apiUrl}/generate-token`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error desconocido");
        }

        const data = await response.json();
        console.log("Token generado:", data.token);
        this.token = data.token; // Muestra el token generado
        this.error = null; // Limpia errores previos
      } catch (error) {
        console.error("Error en la generación del token:", error.message);
        this.error = "No se pudo generar el token. Intenta de nuevo.";
        this.token = null; // Limpia el token si hubo un error
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

.alert {
  text-align: center;
}
</style>
