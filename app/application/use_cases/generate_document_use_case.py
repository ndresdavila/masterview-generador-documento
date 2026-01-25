from app.domain.entities import TemplateData
from app.domain.ports import TemplateRendererPort


class GenerateDocumentUseCase:
    """
    Caso de uso de aplicación encargado de orquestar
    la generación de un documento .docx.
    """

    def __init__(self, template_renderer: TemplateRendererPort) -> None:
        self._template_renderer = template_renderer

    def execute(self, template_name: str, data: dict) -> bytes:
        """
        Ejecuta la lógica:
        - crea la entidad de dominio TemplateData
        - delega al puerto TemplateRendererPort para renderizarla
        """
        template_data = TemplateData(
            template_name=template_name,
            data=data
        )
        result_bytes = self._template_renderer.render(template_data)
        return result_bytes
