from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Query
from ..services.courses.course_service import CourseService
from ..services.module_access_service import ModuleAccessService

router = APIRouter(prefix="/courses", tags=["courses"])
course_service = CourseService()
module_access_service = ModuleAccessService()

# Mock data that matches your frontend structure
MOCK_COURSES_DATA = [
    {
        "id": "python",
        "title": "Python",
        "description": "Aprende programación con Python desde cero hasta conceptos avanzados",
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg",
        "modules": [
            {
                "id": "python-module1",
                "title": "Módulo 1: Fundamentos de Python",
                "description": "En este primer módulo aprenderás los fundamentos esenciales para comenzar a escribir tus propios programas.",
                "lessons": [
                    {"title": "Introducción", "description": "Bienvenida", "route": "/introduction"},
                    {"title": "Lección 1", "description": "¿Qué es programar? ¿Qué es python?", "route": "/lesson1"},
                    {"title": "Lección 2", "description": "Cómo descargar y usar python en tu computador", "route": "/lesson2"},
                    {"title": "Lección 3", "description": "Entrada del usuario, salidas del programa y comentarios", "route": "/lesson3"},
                    {"title": "Lección 4", "description": "Variables y tipos de datos (int, float, str, bool)", "route": "/lesson4"},
                    {"title": "Lección 5", "description": "Operaciones y expresiones", "route": "/lesson5"},
                    {"title": "Reto", "description": "¡Reta tus conocimientos!", "route": "/AssessmentJudge1"},
                    {"title": "Examen", "description": "Prueba tus conocimientos", "route": "/Assessment1"}
                ]
            },
            {
                "id": "python-module2",
                "title": "Módulo 2: Control de flujo",
                "description": "Aprende sobre condicionales, bucles y control de flujo en Python",
                "lessons": [
                    {"title": "Introducción", "description": "Condicionales: if, elif, else", "route": "/introduction-module2"},
                    {"title": "Lección 1", "description": "Condicionales: if, elif, else", "route": "/lesson1-module2"},
                    {"title": "Lección 2", "description": "Ciclo while", "route": "/lesson2-module2"},
                    {"title": "Lección 3", "description": "Ciclo for y range()", "route": "/lesson3-module2"},
                    {"title": "Lección 4", "description": "Combinación de condicionales + bucles + operadores lógicos", "route": "/lesson4-module2"},
                    {"title": "Reto", "description": "¡Reta tus conocimientos!", "route": "/AssessmentJudge2"},
                    {"title": "Examen", "description": "Prueba tus conocimientos", "route": "/assessment2"}
                ]
            }
        ]
    },
    {
        "id": "javascript",
        "title": "JavaScript",
        "description": "Domina JavaScript y el desarrollo web moderno",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png",
        "modules": [
            {
                "id": "js-module1",
                "title": "Módulo 1: Fundamentos de JavaScript",
                "description": "Aprende los conceptos básicos de JavaScript y programación web",
                "lessons": [
                    {"title": "Introducción", "description": "¿Qué es JavaScript?", "route": "/js-introduction"},
                    {"title": "Lección 1", "description": "Variables y tipos de datos", "route": "/js-lesson1"},
                    {"title": "Lección 2", "description": "Funciones en JavaScript", "route": "/js-lesson2"},
                    {"title": "Lección 3", "description": "Objetos y arrays", "route": "/js-lesson3"},
                    {"title": "Lección 4", "description": "DOM y eventos", "route": "/js-lesson4"},
                    {"title": "Proyecto", "description": "Crea tu primera página interactiva", "route": "/js-project1"},
                    {"title": "Examen", "description": "Evaluación del módulo", "route": "/js-assessment1"}
                ]
            },
            {
                "id": "js-module2",
                "title": "Módulo 2: JavaScript Avanzado",
                "description": "Conceptos avanzados y frameworks modernos",
                "lessons": [
                    {"title": "Introducción", "description": "Programación asíncrona", "route": "/js-advanced-intro"},
                    {"title": "Lección 1", "description": "Promises y async/await", "route": "/js-advanced-lesson1"},
                    {"title": "Lección 2", "description": "APIs y fetch", "route": "/js-advanced-lesson2"},
                    {"title": "Lección 3", "description": "Introducción a React", "route": "/js-advanced-lesson3"},
                    {"title": "Proyecto", "description": "Aplicación web completa", "route": "/js-advanced-project"},
                    {"title": "Examen", "description": "Evaluación final", "route": "/js-advanced-assessment"}
                ]
            }
        ]
    },
    {
        "id": "java",
        "title": "Java",
        "description": "Aprende programación orientada a objetos con Java",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/30/Java_programming_language_logo.svg",
        "modules": [
            {
                "id": "java-module1",
                "title": "Módulo 1: Introducción a Java",
                "description": "Fundamentos de Java y programación orientada a objetos",
                "lessons": [
                    {"title": "Introducción", "description": "¿Qué es Java?", "route": "/java-introduction"},
                    {"title": "Lección 1", "description": "Sintaxis básica y variables", "route": "/java-lesson1"},
                    {"title": "Lección 2", "description": "Clases y objetos", "route": "/java-lesson2"},
                    {"title": "Lección 3", "description": "Herencia y polimorfismo", "route": "/java-lesson3"},
                    {"title": "Lección 4", "description": "Manejo de excepciones", "route": "/java-lesson4"},
                    {"title": "Proyecto", "description": "Sistema de gestión simple", "route": "/java-project1"},
                    {"title": "Examen", "description": "Evaluación del módulo", "route": "/java-assessment1"}
                ]
            },
            {
                "id": "java-module2",
                "title": "Módulo 2: Java Avanzado",
                "description": "Conceptos avanzados y desarrollo de aplicaciones",
                "lessons": [
                    {"title": "Introducción", "description": "Colecciones y generics", "route": "/java-advanced-intro"},
                    {"title": "Lección 1", "description": "Streams y programación funcional", "route": "/java-advanced-lesson1"},
                    {"title": "Lección 2", "description": "Multithreading", "route": "/java-advanced-lesson2"},
                    {"title": "Lección 3", "description": "Conexión a bases de datos", "route": "/java-advanced-lesson3"},
                    {"title": "Proyecto", "description": "Aplicación empresarial", "route": "/java-advanced-project"},
                    {"title": "Examen", "description": "Evaluación final", "route": "/java-advanced-assessment"}
                ]
            }
        ]
    }
]

@router.get("/frontend-data", response_model=List[Dict[str, Any]])
async def get_courses_frontend_data() -> List[Dict[str, Any]]:
    """
    Get all courses with their modules and lessons structured for frontend.
    This endpoint returns data in the format expected by the React frontend.
    """
    try:
        # Try to get data from database first
        return await course_service.get_courses_with_modules_and_lessons()
    except Exception as e:
        # If database fails, return mock data
        print(f"Database error: {e}. Returning mock data.")
        return MOCK_COURSES_DATA

@router.get("/frontend-data/mock", response_model=List[Dict[str, Any]])
async def get_courses_frontend_data_mock() -> List[Dict[str, Any]]:
    """
    Get mock courses data for testing purposes.
    This endpoint always returns mock data regardless of database connection.
    """
    return MOCK_COURSES_DATA

@router.get("/frontend-data-with-access", response_model=Dict[str, Any])
async def get_courses_frontend_data_with_access(
    student_email: Optional[str] = Query(None, description="Student email to check module access")
) -> Dict[str, Any]:
    """
    Get all courses with their modules and lessons, including module access information for a specific student.
    
    Args:
        student_email: Optional student email to check module access
        
    Returns:
        Dict containing courses data and module access information
    """
    try:
        # Get courses data
        courses_data = await course_service.get_courses_with_modules_and_lessons()
    except Exception as e:
        # If database fails, use mock data
        print(f"Database error: {e}. Using mock data.")
        courses_data = MOCK_COURSES_DATA
    
    # If no student email provided, return courses without access info
    if not student_email:
        return {
            "courses": courses_data,
            "module_access": None,
            "message": "No student email provided, module access not evaluated"
        }
    
    # Get module access information for the student
    module_access_info = {}
    
    try:
        for course in courses_data:
            course_id = course["id"]
            
            # Special handling for Python course (matches your current frontend logic)
            if course_id == "python":
                python_module2_access = await module_access_service.check_python_module2_access(student_email)
                module_access_info[course_id] = {
                    "python-module1": {"has_access": True, "reason": "First module always accessible"},
                    "python-module2": {
                        "has_access": python_module2_access,
                        "reason": "Requires Assessment1 grade >= 40" if not python_module2_access else "Assessment1 passed"
                    }
                }
            else:
                # For other courses, all modules are accessible for now
                course_access = {}
                for module in course.get("modules", []):
                    module_id = module["id"]
                    course_access[module_id] = {
                        "has_access": True,
                        "reason": "All modules accessible"
                    }
                module_access_info[course_id] = course_access
                
    except Exception as e:
        print(f"Error getting module access: {e}")
        module_access_info = {"error": f"Error evaluating module access: {str(e)}"}
    
    return {
        "courses": courses_data,
        "module_access": module_access_info,
        "student_email": student_email
    } 