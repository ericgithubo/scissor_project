from fastapi import APIRouter,Depends,Request,Response,status,HTTPException,Form
from typing import Annotated
from sqlalchemy.orm import Session
from schemas import Token,LoginForm
from models import Users
#import shortener_app.models as models
import models
from database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import timedelta
from token2 import create_access_token
from oauth2 import get_current_user
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

def get_db():
    """Dependency to get a SQLAlchemy database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bcrpyt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
router = APIRouter(
    prefix="/user",
    tags=["auth"]
)

db_dependency = Annotated[Session,Depends(get_db)]

def authenticate_user(username:str,password:str ,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrpyt_context.verify(password,user.hashed_password):
        return False
    return user


@router.post("/token",response_model=Token)
async def login_for_access_token(response:Response, form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                db:db_dependency):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        return False #"Failed Authentication"
    
    token = create_access_token(user.username,user.id,timedelta(minutes = 60))
    
    response.set_cookie(key="access_Token",value=token,httponly=True)
     
    return True
    #return {
      #  "access_Token":token,
       # "token_type":"bearer"
    #}

@router.get("/login",response_class=HTMLResponse)
async def authenticationpage(request:Request):
   return templates.TemplateResponse("login.html",{"request":request})

@router.post("/",response_class=HTMLResponse)
async def login_user (request:Request,db: db_dependency):
    try:
       form = LoginForm(request)
       await form.create_outh_form()
       response = RedirectResponse(url="/url",status_code = status.HTTP_302_FOUND)
       validate_user_cookie = await login_for_access_token(response = response,form_data=form,db=db) 

       if not validate_user_cookie:
          msg = "invalid username or password"
          return templates.TemplateResponse("login.html",{"request":request,"msg":msg})
       return response
    except HTTPException:
        msg = "unknown error"
        return templates.TemplateResponse("login.html",{"request":request,"msg":msg})

@router.get("/logout",response_class=HTMLResponse)
async def logout(request:Request):
    msg = "logout succesful"
    response = templates.TemplateResponse("login.html",{"request":request,"msg":msg})

    response.delete_cookie(key="access_token")
    return response




    