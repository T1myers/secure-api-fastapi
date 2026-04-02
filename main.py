from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import bcrypt

from database import get_db
from models import User

app = FastAPI()

class UserSchema(BaseModel):
    username: str
    password: str

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = User(username=user.username, password=hashed.decode("utf-8"))
    db.add(new_user)
    db.commit()
    
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    is_valid = bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8"))
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    return {"message": "Login successful"}