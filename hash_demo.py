from fastapi import FastAPI
import bcrypt

app = FastAPI()

@app.get("/show-hash")
def show_hash():
    username = "alice"
    password = "hello123"
    
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    return {
        "username": username,
        "original_password": password,
        "hashed_password": hashed.decode("utf-8")
    }