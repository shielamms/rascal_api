from fastapi import FastAPI

from app.db import create_db_and_tables, init_data
from app.routes.route import api_router


app = FastAPI()

app.include_router(api_router)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()
#     init_data()
