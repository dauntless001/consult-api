from pydantic import BaseSettings
from pathlib import Path


BASE_DIR = Path().absolute()


class Settings(BaseSettings):
    '''Base Settings'''
    ENV: str = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    # quantity of workers for uvicorn
    WORKERS_COUNT: int = 1
    # Enable uvicorn reloading
    RELOAD: bool
    # Database
    DB_ECHO: bool = False
    DB_USER : str
    DB_PASS : str
    DB_NAME : str
    DB_HOST: str
    DB_PORT: int
    DB_TYPE : str

    # Email 
    EMAIL_USERNAME : str
    EMAIL_PASSWORD : str
    EMAIL_FROM : str
    EMAIL_PORT : str
    EMAIL_HOST : str


    
    @property
    def DB_URL(self) -> str:
        """
        Assemble Database URL from settings.

        :return: Database URL.
        """
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"


settings = Settings()