from abc import ABC, abstractmethod
from typing import Dict, Any
from .entities import TemplateData


class TemplateRendererPort(ABC):
    """
    Puerto de dominio: define qué se espera de cualquier adaptador
    que pueda renderizar una plantilla .docx.
    """

    @abstractmethod
    def render(self, template_data: TemplateData) -> bytes:
        """
        Recibe los datos de la plantilla y devuelve el documento
        generado en bytes (.docx).
        """
        raise NotImplementedError
