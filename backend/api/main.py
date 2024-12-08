from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import mlflow
import mlflow.sklearn
import pandas as pd
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import sqlite3
from .models import WeatherInput, UserCreate, UserLogin, Token
import os
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configurations
SECRET_KEY = "your-secret-key-here"  # In production, use a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (email TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Load the ML model
def get_model():
    with open('models/latest_model.txt', 'r') as f:
        run_id = f.read().strip()
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    return model

# Authentication functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/register")
async def register(user: UserCreate):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Check if user exists
    c.execute("SELECT email FROM users WHERE email=?", (user.email,))
    if c.fetchone() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and save user
    hashed_password = pwd_context.hash(user.password)
    c.execute("INSERT INTO users (email, password) VALUES (?, ?)", 
              (user.email, hashed_password))
    conn.commit()
    conn.close()
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE email=?", (form_data.username,))
    result = c.fetchone()
    conn.close()
    
    if not result or not pwd_context.verify(form_data.password, result[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/predict")
async def predict_temperature(weather_input: WeatherInput, token: str = Depends(oauth2_scheme)):
    try:
        # Debug print statements
        print("Attempting to load model...")
        
        # Check if model file exists
        if not os.path.exists('models/latest_model.txt'):
            raise HTTPException(status_code=500, detail="Model file not found. Please train the model first.")
            
        with open('models/latest_model.txt', 'r') as f:
            run_id = f.read().strip()
            print(f"Found run_id: {run_id}")
        
        # Set MLflow tracking URI
        mlflow.set_tracking_uri("http://localhost:5000")
        
        # Load model
        model_uri = f"runs:/{run_id}/model"
        print(f"Loading model from: {model_uri}")
        model = mlflow.sklearn.load_model(model_uri)
        
        # Prepare input data
        input_data = pd.DataFrame([{
            'humidity': weather_input.humidity,
            'pressure': weather_input.pressure,
            'wind_speed': weather_input.wind_speed
        }])
        
        print("Making prediction...")
        prediction = model.predict(input_data)[0]
        return {"predicted_temperature": float(prediction)}
        
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)