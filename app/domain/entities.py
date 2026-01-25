from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TemplateData:
    """
    Entidad de dominio que representa la información mínima
    necesaria para generar un documento a partir de una plantilla.
    """
    template_name: str   # nombre del archivo .docx en /templates
    data: Dict[str, Any] # valores para los placeholders [[ variable ]]
