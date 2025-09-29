from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Auth"
    redis_url: str = "redis://localhost:6379"
    jwt_secret: str = "secret"
    postgres_user: str = "auth-user"
    postgres_password: str = "auth-psw"
    postgres_db: str = "auth-db"
    db_host: str = "localhost"
    db_port: int = 5432

    # Email
    email_host: str = "smtp.mailtrap.io"
    email_port: int = 2525
    email_host_user: str = "auth-user"
    email_host_password: str = "auth-psw"
    email_from: str = "auth@gmail.com"  # TODO: Change to your email

    access_token_expire_minutes: int = 30

    # Google Auth
    google_client_id: str = "google-client-id"
    google_client_secret: str = "google-client-secret"
    google_redirect_url: str = "google-redirect-url"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, extra="ignore"
    )

    @property
    def postgres_url(self) -> str:
        return f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}@{self.db_host}:{self.db_port}/{self.postgres_db}"


settings = Settings()
print(f"settings: {settings.model_dump()}")
