from fastapi import Depends,HTTPException,status,Request
from  fastapi.security import OAuth2PasswordBearer 
from token2 import SECRET_KEY,ALGORITHM
from jose import jwt,JWTError

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(request:Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get("sub")
        user_id:int = payload.get("id")
        if username is None or user_id is None:
            return None
        return{"username":username,"id":user_id}
    except JWTError:
        return "invalid login credentials"
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail=" Authentication Credentials")

    
               
  









    