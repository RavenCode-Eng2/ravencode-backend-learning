from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar routers
from app.api import studentGrades, studentResponses

# Crear una instancia de FastAPI
app = FastAPI(
    title="Student Management API",
    description="API for managing student grades and responses",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplázalo por dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(studentGrades.router, prefix="/grades", tags=["Student Grades"])
app.include_router(studentResponses.router, prefix="/responses", tags=["Student Responses"])

@app.get("/")
async def root():
    """
    Endpoint raíz que retorna un mensaje de bienvenida.
    """
    return {
        "message": "Welcome to the Student Management API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
