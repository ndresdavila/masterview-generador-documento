### Crear entorno virtual:
python -m venv venv

### Acrivar entorno virtual:
venv\Scripts\activate

### Instalar requerimientos:
pip install -r requirements.txt

### Ejecutar microservicio:
uvicorn main:app --reload --port 8100
