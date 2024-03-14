from fastapi import APIRouter,Depends,status,HTTPException,Request,Form
from  sqlalchemy.orm import Session
import schemas,models
from models import Users
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
import database
import bcrypt
from passlib.context import CryptContext


bcrpyt_context= CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="templates")



router = APIRouter()
router = APIRouter(
    prefix="/use",
    tags=["Users"]
)

get_db =database.get_db
db_dependency = Annotated[Session,Depends(get_db)]

@router.post("/",response_model=schemas.ShowUser,status_code=status.HTTP_201_CREATED)
def craete_user(request:schemas.CreateUser,db:Session = Depends(get_db)):
    new_user = models.Users(username = request.username,
                            email = request.email,
                            hashed_password = bcrpyt_context.hash(request.password))
                          

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get("//{id}", response_model=schemas.ShowUser)
def get_user_by_id(id:str,db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code= status. HTTP_404_NOT_FOUND,
                            detail= f"user with id {id} not found")
    return user


