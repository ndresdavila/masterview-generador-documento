import json
import requests
import traceback
from fastapi import APIRouter, HTTPException, Response

from app.interfaces.api.dto import GenerateDocumentRequest
from app.application.use_cases.generate_document_use_case import GenerateDocumentUseCase
from app.infrastructure.templating.docxtpl_renderer import DocxTplTemplateRenderer
from app.config import settings

router = APIRouter(prefix="/documents", tags=["Documents"])

template_renderer = DocxTplTemplateRenderer()
generate_document_use_case = GenerateDocumentUseCase(template_renderer)

# URL del microservicio Zoho Email (desde config/env)
ZOHO_EMAIL_URL = settings.zoho_email_url


# ======================================================
#   ENDPOINT 1: GENERAR DOCX Y DEVOLVERLO
# ======================================================
@router.post(
    "/generate",
    summary="Generar documento DOCX desde plantilla",
    response_description="Archivo .docx generado",
)
async def generate_document(request: GenerateDocumentRequest):
    try:
        # ------ Normalizar saltos de línea ------
        normalized_data = {}
        for key, value in request.data.items():
            if isinstance(value, str):
                normalized_data[key] = value.replace("\r\n", "\n").replace("\r", "\n")
            else:
                normalized_data[key] = value

        # ------ Procesar filas dinámicas (si existen) ------
        rows = normalized_data.get("rows", [])
        processed_rows = []

        for row in rows:
            marks_numbers = row.get("marks_numbers", "")
            container_numbers = row.get("container_numbers", "")
            description = row.get("description", "")
            net_weight = row.get("net_weight", "")
            gross_weight = row.get("gross_weight", "")

            # Crear bloque marks_block
            marks_block = f"CONTAINER:\n{marks_numbers}\nSEALS:\n{container_numbers}"

            # Crear bloque description_block
            description_block = f"{description}\n{net_weight} KN – {gross_weight} KB"

            # Preserve existing row data and add the formatted blocks
            processed_row = row.copy()
            processed_row["marks_block"] = marks_block
            processed_row["description_block"] = description_block

            processed_rows.append(processed_row)

        # Reemplazar filas en los datos del documento
        if rows:
            normalized_data["rows"] = processed_rows

        # ------ Generar Word ------
        doc_bytes = generate_document_use_case.execute(
            template_name=request.template_name, data=normalized_data
        )

        output_filename = f"generado_{request.template_name}"

        return Response(
            content=doc_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"'
            },
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================================================
#   ENDPOINT 2: GENERAR DOCX Y ENVIARLO A ZOHO EMAIL
# ======================================================
@router.post(
    "/generate_and_send",
    summary="Generar un DOCX y enviarlo automáticamente al microservicio Zoho Email",
)
@router.post(
    "/generate_and_send",
    summary="Generar un DOCX y enviarlo automáticamente al microservicio Zoho Email",
)
async def generate_and_send(request: GenerateDocumentRequest):
    try:
        # -------------------------
        # NORMALIZAR SALTOS DE LÍNEA
        # -------------------------
        normalized_data = {}
        for key, value in request.data.items():
            if isinstance(value, str):
                normalized_data[key] = value.replace("\r\n", "\n").replace("\r", "\n")
            else:
                normalized_data[key] = value

        # -------------------------
        # PROCESAR FILAS DINÁMICAS
        # -------------------------
        rows = normalized_data.get("rows", [])
        processed_rows = []

        for row in rows:
            marks_numbers = row.get("marks_numbers", "")
            container_numbers = row.get("container_numbers", "")
            description = row.get("description", "")
            if description:
                # Remove leading whitespace/tabs from each line inside description
                description = "\n".join(
                    [line.lstrip() for line in description.splitlines()]
                )

            net_weight = row.get("net_weight") or 0
            gross_weight = row.get("gross_weight") or 0

            marks_block = f"CONTAINER:\n{marks_numbers}\nSEALS:\n{container_numbers}"

            description_block = f"{description}\n{net_weight} KN – {gross_weight} KB"

            # Preserve existing row data and add the formatted blocks
            processed_row = row.copy()
            processed_row["marks_block"] = marks_block
            processed_row["description_block"] = description_block

            processed_rows.append(processed_row)

        if rows:
            normalized_data["rows"] = processed_rows

        # -------------------------
        # GENERAR DOCUMENTO WORD
        # -------------------------
        doc_bytes = generate_document_use_case.execute(
            template_name=request.template_name, data=normalized_data
        )

        # -------------------------
        # ARMAR PAYLOAD A ZOHO
        # -------------------------
        email_payload = {
            "para": request.email_to or [],
            "cc": request.email_cc or [],
            "cco": request.email_cco or [],
        }

        files = {
            "file": (
                request.template_name,
                doc_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }

        data = {"payload": json.dumps(email_payload)}

        response = requests.post(ZOHO_EMAIL_URL, data=data, files=files)

        if response.status_code != 200:
            print("ERROR EN ZOHO EMAIL:", response.text)
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return {
            "status": "OK",
            "message": "Documento generado y enviado correctamente",
            "zoho_response": response.json(),
        }

    except Exception as e:
        print("\n========== ERROR generate_and_send ==========")
        print("Mensaje:", str(e))
        traceback.print_exc()  # <-- muestra línea exacta del error
        print("============================================\n")

        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
