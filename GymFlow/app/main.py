from fastapi import FastAPI
from app.routes import user_routes, routine_session_routes, auth_routes, routine_routes, exercise_routes,  routine_exercise_routes





app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(routine_routes.router)
app.include_router(exercise_routes.router)
app.include_router(routine_session_routes.router)
app.include_router(routine_exercise_routes.router)
app.include_router(user_routes.router)

@app.get("/")
def root():
    return {"message": "Bienvenido a GymFlow"}
