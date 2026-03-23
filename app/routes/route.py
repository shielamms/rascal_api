from fastapi import APIRouter


from app.routes import event, login, users

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(event.router)


@api_router.get("/")
def read_root():
    """
    Dummy root endpoint to verify API is running. Modify this to return a
    more meaningful response or remove it if not needed.
    """
    return {"message": "Welcome to the API!"}
