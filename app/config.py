from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_username: str
    database_password: str
    database_name: str
    algorithm = str = "HS256"
    secret_key = str
    access_token_expire_minutes: int
    sendgrid_api_key = str
    mailjet_api_key = str
    mailjet_api_secret = str

    class Config:
        env_file = ".env"


settings = Settings()
