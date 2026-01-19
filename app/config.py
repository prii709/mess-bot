from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Google Sheets Configuration
    google_sheets_credentials_path: str = "service_account.json"
    inventory_sheet_id: str
    attendance_sheet_id: str
    feedback_sheet_id: str
    
    # Application Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    low_stock_threshold: int = 10
    low_rating_threshold: float = 2.5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
