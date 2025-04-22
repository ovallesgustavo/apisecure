# Apisecure

API segura construida con FastAPI, PostgreSQL, JWT, Alembic y SQLAlchemy.

## Estructura del Proyecto

- **alembic/**: Migraciones de la base de datos.
- **app/**: Código principal de la aplicación.
  - **api/**: Endpoints de la API.
  - **core/**: Configuración global.
  - **db/**: Modelo de base de datos y sesión.
  - **schemas/**: Esquemas Pydantic.
  - **services/**: Lógica de negocio.
  - **utils/**: Utilidades como JWT.
- **docker-compose.yml**: Configuración de Docker Compose.
- **requirements.txt**: Dependencias del proyecto.

## Instalación

1. Construir y ejecutar los contenedores:

   ```
   docker-compose up --build
   ```

2. Acceder a la API en `http://localhost:8000/docs`.
