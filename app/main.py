from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
import psutil
import os
from app.database import SessionLocal, Metric, Base, engine  # Added database imports

# --- Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY")  # From .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mock user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "adminpass",
    }
}

class Token(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Database Functions ---
def save_metrics_to_db(cpu: float, memory: float):
    db = SessionLocal()
    try:
        metric = Metric(
            cpu_usage=cpu,
            memory_usage=memory,
            timestamp=datetime.utcnow()
        )
        db.add(metric)
        db.commit()
    finally:
        db.close()

# --- Authentication ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Metrics Endpoint ---
@app.get("/metrics")
async def get_metrics(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub"):
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    save_metrics_to_db(cpu, memory)  # Save to PostgreSQL
    
    return {"cpu": cpu, "memory": memory}