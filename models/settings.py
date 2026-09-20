from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    DB_TYPE: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SHINOBI_PROTOCOL: str
    SHINOBI_HOST: str
    SHINOBI_PORT: str
    SHINOBI_API_KEY: str
    SHINOBI_GROUP_KEY: str
    SHINOBI_MONITOR_ID: str
    SHINOBI_DURATION: int

    # Tell Pydantic to read from a .env file
    model_config = SettingsConfigDict(env_file="utils/.env")
    
    def get_settings(self):
        return {
            "DB_TYPE": self.DB_TYPE,
            "DB_HOST": self.DB_HOST,
            "DB_PORT": self.DB_PORT,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
            "DB_NAME": self.DB_NAME,
            "SHINOBI_PROTOCOL": self.SHINOBI_PROTOCOL,
            "SHINOBI_HOST": self.SHINOBI_HOST,
            "SHINOBI_PORT": self.SHINOBI_PORT,
            "SHINOBI_API_KEY": self.SHINOBI_API_KEY,
            "SHINOBI_GROUP_KEY": self.SHINOBI_GROUP_KEY,
            "SHINOBI_MONITOR_ID": self.SHINOBI_MONITOR_ID,
            "SHINOBI_DURATION": self.SHINOBI_DURATION
        }
