from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "apisecure"
    postgres_host: str = "db"
    postgres_port: int = 5432

    secret_key: str = "6d882c138396ffcdcf9c000a67bcd30f59eb711230dfb48c99ccd82e46892361"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    app_env: str = "development"
    
    # Clave de encriptación para el email
    encryption_key: str = "9B7yFgX-fsSMkSsqk4qcb6id1V4xCCg_ZwffBXCnzgE="

    # Configuración de Redis
    redis_host: str = "redis"  # Host de Redis (por defecto "redis" si usas Docker)
    redis_port: int = 6379     # Puerto de Redis
    redis_decode_responses: bool = True  # Decodificar respuestas a strings
    redis_password: str = "password"  # Contraseña de Redis

    class Config:
        env_file = ".env"  # Carga variables desde el archivo .env
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()
