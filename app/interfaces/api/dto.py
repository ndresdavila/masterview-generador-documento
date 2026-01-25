from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class GenerateDocumentRequest(BaseModel):
    template_name: str = Field(
        ...,
        description="Nombre del archivo de plantilla .docx ubicado en la carpeta /templates"
    )
    data: Dict[str, Any] = Field(
        ...,
        description="Diccionario con los valores para los placeholders [[ variable ]]"
    )

    # CAMPOS NUEVOS PARA EL ENVÍO DE EMAIL
    email_to: Optional[List[str]] = Field(
        default=None, description="Lista de correos destino (TO)"
    )
    email_cc: Optional[List[str]] = Field(
        default=None, description="Lista de correos CC"
    )
    email_cco: Optional[List[str]] = Field(
        default=None, description="Lista de correos CCO"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "template_name": "bill_of_lading.docx",
                "data": {
                    "shipper": "MASTER FREIGHT",
                    "consignee": "IMPORTACIONES XYZ",
                    "booking_number": "BK-123",
                    "bill_of_lading_number": "BL-001-2025"
                },
                "email_to": ["cindy.moya@outlook.com"],
                "email_cc": ["control@masterview.me"],
                "email_cco": []
            }
        }
