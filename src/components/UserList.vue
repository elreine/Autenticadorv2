<template>
    <div>
      <h2>Usuarios Registrados</h2>
      <ul>
        <li v-for="user in users" :key="user.username">{{ user.username }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        users: []
      };
    },
    mounted() {
      // Recuperar la lista de usuarios al cargar el componente
      fetch("https://autenticadorv2.onrender.com/users")
        .then(response => response.json())
        .then(data => {
          this.users = data.users;
        })
        .catch(error => console.error("Error al cargar usuarios:", error));
    }
  };
  </script>
  
  <style scoped>
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    padding: 5px;
    background-color: #f0f0f0;
    margin: 5px 0;
    border-radius: 4px;
  }
  </style>
  