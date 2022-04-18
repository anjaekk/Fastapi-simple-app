from os import getenv
from dotenv import load_dotenv
from datetime import datetime, timedelta
from jose import JWTError, jwt

env = load_dotenv()


JWT_SECRET = getenv('JWT_SECRET')
ALGORITHM = getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE = getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(user_id):
    payload = {'id': user_id}
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE))
    payload['exp'] = expire
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)