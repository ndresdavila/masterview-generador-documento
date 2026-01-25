import io
from pathlib import Path
from typing import Optional

from docxtpl import DocxTemplate
from jinja2 import Environment

from app.domain.entities import TemplateData
from app.domain.ports import TemplateRendererPort


class DocxTplTemplateRenderer(TemplateRendererPort):
    """
    Adaptador de infraestructura que usa docxtpl + Jinja2
    para renderizar plantillas .docx con placeholders [[ variable ]].
    """

    def __init__(self, templates_dir: Optional[str] = None) -> None:
        # Directorio donde se almacenan las plantillas .docx
        if templates_dir is None:
            # Por defecto: carpeta "templates" en la raíz del proyecto
            self._templates_dir = Path(__file__).resolve().parents[3] / "templates"
        else:
            self._templates_dir = Path(templates_dir)

        # Configuración de Jinja2 para usar [[ ]] en lugar de {{ }}
        self._jinja_env = Environment(
            autoescape=False, variable_start_string="[[", variable_end_string="]]"
        )

    def render(self, template_data: TemplateData) -> bytes:
        template_path = self._templates_dir / template_data.template_name

        if not template_path.exists():
            raise FileNotFoundError(f"No se encontró la plantilla: {template_path}")

        # Cargar plantilla
        doc = DocxTemplate(str(template_path))

        # Renderizar con el contexto de datos y el entorno Jinja2
        doc.render(template_data.data, jinja_env=self._jinja_env)

        # Guardar en memoria (no en disco)
        output_stream = io.BytesIO()
        doc.save(output_stream)
        output_stream.seek(0)

        return output_stream.read()
