from fastapi import FastAPI
from routes.emociones import emociones_router

app = FastAPI()

app.include_router(emociones_router)