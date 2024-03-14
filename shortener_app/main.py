from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from routers import users,scissors,login
import models
from routers.scissors import router
from starlette.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

models .Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(scissors.router)
app.include_router(login.router)






