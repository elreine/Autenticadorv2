<template>
    <div class="container mt-3">
      <button class="btn btn-primary w-100" @click="generateToken">Generar Token</button>
      <div v-if="token" class="mt-3 alert alert-success">
        <h5 class="text-center">Tu Token:</h5>
        <code class="d-block bg-light p-2 text-center">{{ token }}</code>
      </div>
      <div v-if="error" class="mt-3 alert alert-danger">
        <h5 class="text-center">Error:</h5>
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
        const apiUrl = this.$apiUrl || "http://127.0.0.1:5000";
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
          this.token = data.token; // Asignar token generado
          this.error = null; // Limpiar errores previos
        } catch (error) {
          console.error("Error al generar token:", error.message);
          this.error = "No se pudo generar el token. Intenta de nuevo.";
          this.token = null; // Limpiar token en caso de error
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
  