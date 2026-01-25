from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.interfaces.api.router import router

app = FastAPI(title="Generador Proforma Word")

# -----------------------------------------------------------------
# HABILITAR CORS (ANTES DE INCLUIR LAS RUTAS)
# -----------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Puedes poner ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],     # <--- ESTO PERMITE OPTIONS
    allow_headers=["*"],
)

# -----------------------------------------------------------------
# INCLUIR RUTAS
# -----------------------------------------------------------------
app.include_router(router)
