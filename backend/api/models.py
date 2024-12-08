from pydantic import BaseModel

class WeatherInput(BaseModel):
    humidity: float
    pressure: float
    wind_speed: float

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str