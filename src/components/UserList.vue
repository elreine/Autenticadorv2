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
    fetch("https://autenticadorv2.onrender.com/users")
      .then((response) => response.json())
      .then((data) => {
        this.users = data.users;
      })
      .catch((error) => console.error("Error al cargar usuarios:", error));
  },
};
</script>

<style scoped>
.table {
  margin: auto;
  max-width: 80%;
}
</style>
