from typing import Optional

from pydantic import BaseSettings


class NaverClovaConig(BaseSettings):
    CLOVA_HOST: Optional[str] = None
    CLOVA_API_KEY: Optional[str] = None
    CLOVA_PRIMARY_KEY: Optional[str] = None
    CLOVA_REQUEST_ID: Optional[str] = None

    class Config:
        env_file: str = ".env"


clova_config = NaverClovaConig()
