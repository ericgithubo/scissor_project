from pydantic import BaseModel, HttpUrl
from typing_extensions import Optional
from fastapi import FastAPI,Response,Request

class URLBase(BaseModel):
    long_url: str
    custom_url: Optional[str] = None

class ShortenUrl(URLBase):
    clicks: Optional[int] = None

class ShowUser(BaseModel):
    username:str
    email:str
    class config():
        from_attributes = True

class CreateUser(BaseModel):
    username:str
    email:str
    password:str

class Token(BaseModel):
    access_Token:str
    token_type:str

class LoginForm:
    def __init__(self,request:Request):
        self.request:Request = request
        self.username:Optional[str] = None
        self.password:Optional[str] = None

    async def create_outh_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")







