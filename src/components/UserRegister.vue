<template>
  <div>
    <h2>Registro de Usuario</h2>
    <form @submit.prevent="register">
      <label for="username">Usuario:</label>
      <input type="text" v-model="username" required />

      <label for="password">Contraseña:</label>
      <input type="password" v-model="password" @input="validatePassword" required />
      <p>{{ passwordStrength }}</p>

      <button type="submit" :disabled="!isPasswordValid">Registrar</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      passwordStrength: '',
      isPasswordValid: false,
      csrfToken: '' // Nueva propiedad para almacenar el token CSRF
    };
  },
  methods: {
    // Método para obtener el token CSRF
    fetchCsrfToken() {
      fetch("https://autenticadorv2.onrender.com/csrf-token")
        .then(response => response.json())
        .then(data => {
          this.csrfToken = data.csrf_token;
        })
        .catch(error => console.error("Error al obtener el token CSRF:", error));
    },

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
      // Enviar solicitud POST al backend con el token CSRF
      fetch("https://autenticadorv2.onrender.com/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRF-Token": this.csrfToken // Incluir el token CSRF en el encabezado
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.message) {
          alert(data.message);
        } else if (data.error) {
          alert(data.error);
        }
      })
      .catch(error => {
        console.error("Error:", error);
        alert("Hubo un problema con el registro.");
      });
    }
  },

  // Llamamos a fetchCsrfToken cuando el componente se monte
  mounted() {
    this.fetchCsrfToken();
  }
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: auto;
}

label, input, button {
  margin-top: 10px;
}

p {
  color: green;
}
</style>
