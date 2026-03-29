from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt

app = FastAPI()
users_db = {}


class User(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    users_db[user.username] = hashed
    
    print("Username:", user.username)
    print("Hashed password:", hashed)
    
    return {"message": "User registered successfully"}


# 🔐 LOGIN
@app.post("/login")
def login(user: User):
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="User not found")

    is_valid = bcrypt.checkpw(user.password.encode("utf-8"), users_db[user.username])
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return {"message": "Login successful"}

