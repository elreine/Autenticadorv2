<template>
    <div class="container mt-5">
      <h2>Generar Token</h2>
      <p>Haz clic en el botón para generar un token único:</p>
      <button class="btn btn-primary" @click="generateToken">Generar Token</button>
      <div v-if="token" class="mt-3">
        <h5>Token Generado:</h5>
        <input type="text" class="form-control" v-model="token" readonly />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        token: "", // Almacena el token generado
      };
    },
    methods: {
      generateToken() {
        fetch("https://autenticadorv2.onrender.com/generate-token")
          .then((response) => response.json())
          .then((data) => {
            this.token = data.token; // Asigna el token a la variable
          })
          .catch((error) => {
            console.error("Error al generar el token:", error);
            alert("Hubo un problema al generar el token.");
          });
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: auto;
  }
  </style>
  