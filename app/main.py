from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.core.metrics import REQUEST_COUNT, RESPONSE_TIME, ERROR_COUNT

import time

# Import routers
from .api import studentGrades, studentResponses, lessons, assessments, progress, courses_frontend, module_access, roadmaps

# Create FastAPI instance
app = FastAPI(
    title="Learning Platform Evaluation Service",
    description="Evaluation service for managing courses, modules, lessons, assessments, and student progress evaluation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(studentGrades.router)
app.include_router(studentResponses.router)
app.include_router(lessons.router)
app.include_router(assessments.router)
app.include_router(progress.router)
app.include_router(courses_frontend.router)
app.include_router(module_access.router)
app.include_router(roadmaps.router)

# Middleware para registrar métricas
@app.middleware("http")
async def record_metrics(request, call_next):
    method = request.method
    endpoint = request.url.path

    # Registrar la hora de inicio para medir el tiempo de respuesta
    start_time = time.time()

    # Continuar con la solicitud
    response = await call_next(request)

    # Medir tiempo de respuesta
    duration = time.time() - start_time
    RESPONSE_TIME.labels(method=method, endpoint=endpoint).observe(duration)

    # Incrementar contador de peticiones
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()

    # Si hay un error (código de estado >= 400), aumentar el contador de errores
    if response.status_code >= 400:
        ERROR_COUNT.labels(method=method, endpoint=endpoint).inc()

    return response

# Ruta para exponer las métricas en formato Prometheus
@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)




@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to the Learning Platform Evaluation Service",
        "service": "evaluation",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
