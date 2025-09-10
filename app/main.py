from fastapi import FastAPI

app = FastAPI(title = "Japanese Word Repetition API", version = "0.1")

@app.get("/")
def root():
    return {"message": "Japanese Word Repetition API работает!"}

@app.get("/hello")
def say_hello(name: str = "User"):
    return {"message": f"Привет, {name}!"}