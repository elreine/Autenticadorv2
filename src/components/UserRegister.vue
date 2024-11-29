<template>
  <div class="container mt-5">
    <h2 class="text-center">Registro</h2>
    <form @submit.prevent="register">
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
          @input="validatePassword"
          required
        />
        <p class="text-muted">{{ passwordStrength }}</p>
      </div>
      <div class="mb-3">
        <label for="token" class="form-label">Token</label>
        <input
          type="text"
          class="form-control"
          id="token"
          v-model="token"
          placeholder="Ingresa tu token"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="!isPasswordValid || !token">
        Registrarse
      </button>
    </form>
    <p class="mt-3">
      ¿Ya tienes cuenta?
      <router-link to="/login">Inicia sesión aquí</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      token: "", // Token manual ingresado por el usuario
      passwordStrength: "",
      isPasswordValid: false,
    };
  },
  methods: {
    validatePassword() {
      const password = this.password;
      const hasUpperCase = /[A-Z]/.test(password);
      const hasNumber = /[0-9]/.test(password);
      const hasSpecialChar = /[!@#$%^&*()_+\-={}|;:'",.<>?]/.test(password);
      const isLongEnough = password.length >= 8;

      let feedbackMessage = "La contraseña debe tener al menos:";
      let isPasswordValid = true;

      if (!isLongEnough) {
        feedbackMessage += " 8 caracteres,";
        isPasswordValid = false;
      }
      if (!hasUpperCase) {
        feedbackMessage += " una letra mayúscula,";
        isPasswordValid = false;
      }
      if (!hasNumber) {
        feedbackMessage += " un número,";
        isPasswordValid = false;
      }
      if (!hasSpecialChar) {
        feedbackMessage += " un carácter especial,";
        isPasswordValid = false;
      }

      if (isPasswordValid) {
        this.passwordStrength = "Contraseña segura";
        this.isPasswordValid = true;
      } else {
        this.passwordStrength = feedbackMessage.slice(0, -1) + ".";
        this.isPasswordValid = false;
      }
    },
    register() {
      if (!this.token) {
        alert("Por favor, genera un token antes de registrarte.");
        return;
      }

      fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Registration-Token": this.token, // Enviar el token
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            alert(data.message);
            this.username = "";
            this.password = "";
            this.token = ""; // Limpiar el token
          } else if (data.error) {
            alert(data.error);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          alert("Hubo un problema con el registro.");
        });
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: auto;
}
</style>
