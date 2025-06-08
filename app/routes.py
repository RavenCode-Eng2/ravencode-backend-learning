from fastapi import APIRouter
from app.database import lecciones
from app.models import Leccion

router = APIRouter()

@router.get("/lecciones")
def listar_lecciones():
    return list(lecciones.find({}, {"_id": 0}))

@router.post("/lecciones")
def crear_leccion(leccion: Leccion):
    lecciones.insert_one(leccion.dict())
    return {"mensaje": "Lección creada"}
