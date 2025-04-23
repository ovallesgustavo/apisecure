# 🚀 Apisecure

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Apisecure** es una API segura y escalable construida con FastAPI, PostgreSQL, JWT, Alembic y SQLAlchemy.  
Diseñada para ofrecer autenticación avanzada, gestión de tokens y protección de datos sensibles.

---

## 📁 Estructura del Proyecto
```code
alembic/ Migraciones de la base de datos
app/ Código principal de la aplicación
├── api/ Endpoints
├── core/ Configuración global y settings
├── db/ Modelos y sesión de base de datos
├── schemas/ Esquemas Pydantic para validación
├── services/ Lógica de negocio y reglas
└── utils/ Utilidades (JWT, helpers, etc.)
docker-compose.yml Configuración para levantar contenedores Docker
requirements.txt Dependencias del proyecto
```

---

## ⚙️ Instalación & Ejecución Local

1. Clona el repositorio y navega al directorio del proyecto.
```code
git clone https://github.com/ovallesgustavo/apisecure.git
```

2. Construye y levanta los contenedores Docker:
```code
docker-compose up --build
```
3. Ejecuta las migraciones dentro del contenedor para sincronizar la base de datos:
```code
docker-compose exec app alembic upgrade head
```
4. Accede a la documentación interactiva de la API en:

[http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Características Destacadas

- **Autenticación con JWT**  
  Access Token y Refresh Token para sesiones seguras.

- **Rotación Automática de Tokens**  
  Renovación sin necesidad de re-login constante.

- **Lista Negra de Tokens (Blacklist)**  
  Revocación de tokens usando Redis.

- **Encriptación del Payload Sensible**  
  Protección extra para datos críticos.

- **Validación Avanzada de Contraseñas**  
  Expresiones regulares para políticas robustas.

---

## 🤝 Contribuciones

¡Contribuciones y mejoras son bienvenidas!  
Por favor, abre issues o pull requests para colaborar.

---

## ⚖️ Licencia

Este proyecto está bajo licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

---

> **Apisecure** — Construye APIs seguras y escalables con confianza. 🚀