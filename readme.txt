**Sistema de Autenticación con Validación de Contraseñas y Encriptación**
Descripción
Este proyecto es un sistema de autenticación con validación de contraseñas en el frontend (Vue.js) y encriptación en el backend (Flask y Firebase). Permite a los usuarios registrarse y guarda sus contraseñas de forma segura.

Tecnologías Utilizadas
Frontend: Vue.js, desplegado en Vercel
Backend: Flask (Python), con Firebase como base de datos, desplegado en Render
Seguridad: CSRF Token y encriptación de contraseñas con bcrypt

Instrucciones para Ejecutar el Proyecto Localmente
Clonar el Repositorio:

-git clone <URL_DEL_REPOSITORIO>
-cd autenticador
-Configurar el Backend:

Añadir el archivo firebase_key.json en el directorio correcto.
Crear un entorno virtual e instalar las dependencias:
-python -m venv venv
-source venv/bin/activate  # En Windows usa venv\Scripts\activate
-pip install -r requirements.txt

Configurar el Frontend:
Instalar dependencias de Vue:
-npm install

Ejecutar Localmente:
Backend:
-python backend/app.py
Frontend:
-npm run serve

Acceso al Proyecto Desplegado
Frontend en Vercel: https://autenticadorv2-qcxr86mx9-reinels-projects-b1028227.vercel.app
Backend en Render: Conectado automáticamente al frontend en Vercel

"Funcionalidades Principales"
Registro de Usuario: Validación en tiempo real de contraseñas en el frontend.
Encriptación de Contraseñas: Utiliza bcrypt en el backend para encriptar y almacenar contraseñas en Firebase.
Medidas de Seguridad: Implementación de CSRF y validación de entrada para prevenir vulnerabilidades.