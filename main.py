# moin.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.emociones import emociones_router

app = FastAPI()

# Configurar CORS para permitir peticiones desde cualquier IP local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las direcciones (o puedes limitarlo a tu frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir el router de emociones
app.include_router(emociones_router)
