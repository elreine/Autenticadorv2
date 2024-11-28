<template>
  <div>
    <h2 class="text-center">Usuarios Registrados</h2>
    <table class="table table-striped mt-4">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuario</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="user.username">
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
      users: [],
    };
  },
  mounted() {
    const token = localStorage.getItem("sessionToken");
    if (!token) {
      alert("Acceso denegado. Por favor, inicia sesión.");
      this.$router.push("/login");
      return;
    }

    fetch("https://autenticadorv2.onrender.com/users", {
      headers: {
        "X-Session-Token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          this.$router.push("/login");
        } else {
          this.users = data.users;
        }
      })
      .catch((error) => {
        console.error("Error al cargar usuarios:", error);
        alert("Hubo un problema al obtener la lista de usuarios.");
      });
  },
};
</script>

<style scoped>
.table {
  margin: auto;
  max-width: 80%;
}
</style>
