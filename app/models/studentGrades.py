from pydantic import BaseModel, Field
from typing import List

class StudentGrades(BaseModel):
    """
    Representa las calificaciones de un estudiante para un módulo específico.

    Attributes:
        email (str): Token único asignado al estudiante.
        module (str): El nombre del módulo.
        grade (float): La calificación obtenida en el módulo.
        date_assigned (str): La fecha en que se asignó la calificación.
    """
    email: str = Field(..., description="Token único del estudiante")
    module: str = Field(..., description="Nombre del módulo")
    grade: float = Field(..., description="Calificación obtenida en el módulo")
    date_assigned: str = Field(..., description="Fecha de asignación de la calificación")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "token123",
                "module": "Math101",
                "grade": 95.0,
                "date_assigned": "2025-06-08"
            }
        }
    }
