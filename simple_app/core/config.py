from os import getenv, path
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
env = load_dotenv()

class Settings(BaseModel):
    authjwt_secret_key: str = getenv('SECRET_KEY')

@AuthJWT.load_config
def get_config():
    return Settings()