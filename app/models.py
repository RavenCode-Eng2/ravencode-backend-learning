from pydantic import BaseModel
from typing import List

class Leccion(BaseModel):
    curso: str
    tema: str
    titulo: str
    contenido_html: str

class Pregunta(BaseModel):
    curso: str
    tema: str
    pregunta: str
    opciones: List[str]
    respuesta_correcta: int
