from typing import Optional
from pymongo.results import InsertOneResult, UpdateResult
from app.models.studentGrades import StudentGrades  # Importamos el modelo correcto
from app.DB.database import get_database

class GradesService:
    """
    Service for managing student grades in the database.
    Handles all operations related to storing and updating student grades.
    """

    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Could not connect to the database")
        self.collection = self.db["student_grades"]

    def create_or_update_grades(self, student_grades: StudentGrades) -> dict:
        """
        Create or update the student's grade in the database.
        If the student already has grades for a specific module, update them.
        """
        # Buscar si la calificación para este estudiante y módulo ya existe
        existing_grades = self.get_grades_by_token(student_grades.student_token, student_grades.module)

        if existing_grades:
            # Si la calificación ya existe, se actualiza
            update_data = student_grades.dict(exclude_unset=True)
            result = self.collection.update_one(
                {"student_token": student_grades.student_token, "module": student_grades.module},
                {"$set": update_data}
            )
            return {"message": "Grade updated successfully", "updated_count": result.modified_count}
        else:
            # Si no existe, se crea una nueva entrada
            result = self.collection.insert_one(student_grades.dict())
            return {"message": "Grade created successfully", "inserted_id": str(result.inserted_id)}

    def get_grades_by_token(self, student_token: str, module: str) -> Optional[dict]:
        """
        Retrieve student grades by their token and module.
        """
        student_grades = self.collection.find_one({"student_token": student_token, "module": module})
        if student_grades:
            student_grades["_id"] = str(student_grades["_id"])  # Convertimos el ObjectId a string
        return student_grades

    def list_grades(self) -> list:
        """
        List all grades in the database.
        """
        grades = list(self.collection.find())
        return [{**grade, "_id": str(grade["_id"])} for grade in grades]
