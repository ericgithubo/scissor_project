from jose import jwt
from datetime import timedelta,datetime
from models import Users




SECRET_KEY = "e6d40f0cd8ad70913046a5ea2603c37480c377561769d0f826e159b50e9ef8e9"
ALGORITHM = "HS256"

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode = {"sub":username,"id":user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)