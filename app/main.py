from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
