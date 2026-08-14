from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgres://challenge:challenge@postgres:5432/challenge?sslmode=disable"
    cors_origins: str = "http://localhost:15173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
