from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    sqlserver_connection_string: str = Field(default="Data Source=localhost\\SQLEXPRESS;Initial Catalog=BaseCoreSales;Integrated Security=True;Encrypt=True;Trust Server Certificate=True", alias="SQLSERVER_CONNECTION_STRING")
    jwt_secret: str = Field(default="dev-secret", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=60 * 12, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    cors_origins: str = Field(default="http://localhost:5173", alias="CORS_ORIGINS")

    class Config:
        env_file = ".env"
        populate_by_name = True

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()