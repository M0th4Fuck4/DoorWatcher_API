from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DB_TYPE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Tell Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file="utils/.env")
    
    def get_settings(self):
        return {
            "DB_TYPE": self.DB_TYPE,
            "DB_HOST": self.DB_HOST,
            "DB_PORT": self.DB_PORT,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
            "DB_NAME": self.DB_NAME
        }
