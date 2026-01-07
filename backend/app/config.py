from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
                                            
    
              
    database_url: str = "postgresql://postgres:postgres@localhost:5432/analytics"
    
         
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
                   
    model_storage_type: str = "local"                      
    model_storage_path: str = "./models"
    s3_bucket_name: Optional[str] = None
    s3_region: str = "us-east-1"
    
         
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
                 
    environment: str = "development"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
