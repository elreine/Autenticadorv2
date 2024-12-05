const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/": {
        target: "http://127.0.0.1:5000", // Redirige al backend
        ws: false, // Desactiva WebSockets
        changeOrigin: true,
      },
    },
  },
});
