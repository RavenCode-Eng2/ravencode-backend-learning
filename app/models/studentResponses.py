from pydantic import BaseModel, Field
from typing import List

class Response(BaseModel):
    """
    Representa una respuesta de un estudiante a una pregunta del examen.

    Attributes:
        question_id (int): Identificador único de la pregunta.
        answer (str): Respuesta seleccionada por el estudiante.
    """
    question_id: int = Field(..., description="ID de la pregunta")
    answer: str = Field(..., description="Respuesta seleccionada por el estudiante")

class StudentResponses(BaseModel):
    """
    Representa las respuestas de un estudiante a un conjunto de preguntas.

    Attributes:
        email (str): Token único asignado al estudiante.
        responses (List[Response]): Lista de respuestas con sus respectivos identificadores de pregunta.
    """
    email: str = Field(..., description="Token único del estudiante")
    responses: List[Response] = Field(..., description="Lista de respuestas del estudiante")

    class Config:
        schema_extra = {
            "example": {
                "email": "abcd1234",
                "responses": [
                    {"question_id": 1, "answer": "a"},
                    {"question_id": 2, "answer": "b"},
                    {"question_id": 3, "answer": "c"}
                ]
            }
        }
