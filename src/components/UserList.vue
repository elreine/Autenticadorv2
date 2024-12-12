<template>
  <div class="container mt-5">
    <h2 class="text-center">Usuarios Registrados</h2>
    <table class="table table-striped mt-4">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuario</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="index">
          <td>{{ index + 1 }}</td>
          <td>{{ user.username }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [], // Lista de usuarios obtenida del backend
    };
  },
  methods: {
    async fetchUsers() {
      const token = localStorage.getItem("sessionToken");
      if (!token) {
        alert("Acceso denegado. Por favor, inicia sesión.");
        this.$router.push("/login");
        return;
      }

      try {
        const apiUrl = this.$apiUrl; // Usar la URL global configurada en main.js
        const response = await fetch(`${apiUrl}/users`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-Session-Token": token, // Enviar el token para autenticar la solicitud
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || "Error al obtener usuarios");
        }

        const data = await response.json();
        this.users = data.users; // Guardar la lista de usuarios en la data
      } catch (error) {
        console.error("Error al cargar usuarios:", error.message);
        alert("Hubo un problema al obtener la lista de usuarios. " + error.message);
        this.$router.push("/login");
      }
    },
  },
  mounted() {
    this.fetchUsers(); // Cargar usuarios al montar el componente
  },
};
</script>

<style scoped>
.table {
  margin: auto;
  max-width: 80%;
}
</style>
