from fastapi import FastAPI
from app.routes import auth_routes, session_routes, routine_routes


app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(session_routes.router)
app.include_router(routine_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a GymFlow"}
