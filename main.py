from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Response
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


@app.get("/health")
def health():
    template = Path(__file__).resolve().parent / "templates" / "Template.docx"
    if not template.is_file():
        return Response(content='{"ok":false}', media_type="application/json", status_code=503)
    return {"ok": True}
