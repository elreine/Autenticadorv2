<template>
  <div class="container mt-5">
    <h2 class="text-center">Registro</h2>
    <form @submit.prevent="register">
      <!-- Usuario -->
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

      <!-- Contraseña -->
      <div class="mb-3">
        <label for="password" class="form-label">Contraseña</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="password"
          @input="validatePassword"
          placeholder="Ingrese la contraseña"
          required
        />
      </div>
      <!-- Mensaje de Validación -->
      <p
        class="text-muted mb-3"
        :class="{ 'text-success': isPasswordValid, 'text-danger': !isPasswordValid }"
      >
        {{ passwordStrength }}
      </p>

      <!-- Token -->
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

      <!-- Botón de Registro -->
      <button
        type="submit"
        class="btn btn-primary w-100"
        :disabled="!isPasswordValid || !username || !token"
      >
        Registrarse
      </button>
    </form>

    <!-- Enlace a Iniciar Sesión -->
    <p class="mt-3 text-center">
      ¿Ya tienes cuenta?
      <router-link to="/login" class="text-primary fw-bold">
        Inicia sesión aquí
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
      token: "",
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

      let feedbackMessage = "La contraseña debe incluir:";
      let isValid = true;

      if (!isLongEnough) {
        feedbackMessage += " al menos 8 caracteres,";
        isValid = false;
      }
      if (!hasUpperCase) {
        feedbackMessage += " una letra mayúscula,";
        isValid = false;
      }
      if (!hasNumber) {
        feedbackMessage += " un número,";
        isValid = false;
      }
      if (!hasSpecialChar) {
        feedbackMessage += " un carácter especial,";
        isValid = false;
      }

      if (isValid) {
        this.passwordStrength = "Contraseña segura";
        this.isPasswordValid = true;
      } else {
        this.passwordStrength = feedbackMessage.slice(0, -1) + ".";
        this.isPasswordValid = false;
      }
    },

    async register() {
      const apiUrl = process.env.VUE_APP_API_URL || "http://127.0.0.1:5000";

      try {
        const response = await fetch(`${apiUrl}/register`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Registration-Token": this.token,
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error desconocido");
        }

        // Registro exitoso
        alert("Registro exitoso. Ahora puedes iniciar sesión.");
        this.$router.push("/login");
      } catch (error) {
        console.error("Error en el registro:", error.message);
        alert("No se pudo completar el registro. Intenta nuevamente.");
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

.text-muted {
  font-size: 0.9rem;
  margin-top: -10px; /* Ajusta el espaciado del mensaje */
}

.text-danger {
  color: #dc3545;
}

.text-success {
  color: #198754;
}
</style>
