<template>
    <div>
      <h2>Usuarios Registrados</h2>
      <p v-if="isLoading">Cargando...</p>
      <ul v-else>
        <li v-for="user in users" :key="user.username">{{ user.username }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        users: [],
        isLoading: true // Nuevo estado de carga
      };
    },
    mounted() {
      this.isLoading = true;
      fetch("https://autenticadorv2.onrender.com/users")
        .then(response => response.json())
        .then(data => {
          this.users = data.users;
          this.isLoading = false;
        })
        .catch(error => {
          console.error("Error al cargar usuarios:", error);
          this.isLoading = false;
        });
    }
  };
  </script>
  
  <style scoped>
  ul {
  list-style-type: none;
  padding: 0;
  max-width: 300px;
  margin: auto;
}

li {
  padding: 10px;
  background-color: #e0f7fa;
  margin: 5px 0;
  border-radius: 4px;
  text-align: center;
  font-weight: bold;
  color: #00796b;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
}

  </style>
  