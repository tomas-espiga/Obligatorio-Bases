Sistema de Reservas de Salas - Obligatorio BD1

Cómo ejecutar el proyecto.

A continuación están los pasos necesarios para levantar la aplicación desde cero.


1. Requisitos

Antes de empezar, es necesario tener instalado:

Python 3.10+

MySQL Server 8

Git y VS Code


2. Crear la base de datos

Abrir la terminal de MySQL:

"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p


Crear la base y cargar el esquema:

mysql -u root -p < db/schema.sql


Cargar los datos de ejemplo:

mysql -u root -p < db/sample_data.sql


La base debe quedar creada con el nombre:

Obligatorio


3. Configurar la conexión a MySQL

En el archivo:

app/config.py


Modificar según corresponda:

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "TU_PASSWORD"
DB_NAME = "Obligatorio"


4. Crear y activar el entorno virtual

Desde la carpeta del proyecto:

cd obligatorio_salas_app
cd app

Windows:
python -m venv venv
venv\Scripts\activate


5. Instalar dependencias
pip install -r requirements.txt

6. Ejecutar la aplicación

Desde dentro de la carpeta app/:

flask --app app/app.py run --debug


7. Abrir la aplicación en el navegador
http://127.0.0.1:5000/


8. Usuarios para probar el login

Los datos están en la tabla login. Los valores incluidos en sample_data.sql son:

juan.perez@ucu.edu.uy
 -hash1

maria.gomez@ucu.edu.uy
 -hash2

roberto.suarez@ucu.edu.uy
 -hash3


9. Pruebas básicas recomendadas

Crear participantes y editar/eliminar.

Crear salas y modificar capacidad o tipo.

Intentar hacer reservas con superpocisiones de turno.

Verificar límite de 2 reservas diarias.

Verificar límite de 3 reservas activas por semana.

Crear y eliminar sanciones.


10. Estructura del proyecto
obligatorio_salas_app/
│
├── app/
│   ├── app.py
│   ├── db.py
│   ├── templates/
│   ├── static/
│   └── config.py
│
├── db/
│   ├── schema.sql
│   └── sample_data.sql
│
├── Dockerfile
├── docker-compose.yml
└── README.md