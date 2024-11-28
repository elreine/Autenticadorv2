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
      fetch("https://autenticadorv2.onrender.com/generate-token", {
        method: "GET",
        headers: {
          "X-Auth-Key": "mi_clave_segura",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.token) {
            this.token = data.token;
            localStorage.setItem("registrationToken", data.token); // Guardar el token
          } else if (data.error) {
            alert(data.error);
          }
        })
        .catch((error) => console.error("Error al generar el token:", error));
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
