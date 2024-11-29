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
      fetch("http://127.0.0.1:5000/generate-token", {
        method: "GET",
        headers: {
          "X-Auth-Key": "mi_clave_secreta", // Cambiar a la clave correcta
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.token) {
            this.token = data.token; // Guarda el token generado
            localStorage.setItem("registrationToken", data.token); // Guardar el token en localStorage
            alert("Token generado con éxito: " + data.token);
          } else if (data.error) {
            alert(data.error); // Mostrar errores enviados desde el backend
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
