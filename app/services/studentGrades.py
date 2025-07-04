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

    def create_grade(self,student_grades: StudentGrades) -> dict:
        """
        Create  the student's grade in the database.
        """
        email = student_grades.email.strip()
        module = student_grades.module.strip()
        existing_grades = self.get_grades_by_email(email, module)
        if not existing_grades:
            # Si no existe, se crea una nueva entrada
            data = student_grades.dict()
            data['email'] = email
            data['module'] = module
            result = self.collection.insert_one(data)
            return {"message": "Grade created successfully", "inserted_id": str(result.inserted_id)}
        


    def update_grades(self, student_grades: StudentGrades) -> dict:
        """
        Update the student's grade in the database.
        If the student already has grades for a specific module, update them.
        """
        email = student_grades.email.strip()
        module = student_grades.module.strip()
        existing_grades = self.get_grades_by_email(email, module)

        if existing_grades:
            # Si la calificación ya existe, se actualiza
            update_data = {"grade": student_grades.grade}
            result = self.collection.update_one(
                {"email": email, "module": module},
                {"$set": update_data}
            )
            return {"message": "Grade updated successfully", "updated_count": result.modified_count}
        return {"message": "Grade not found"}


    def get_grades_by_email(self, email: str, module: str) -> Optional[dict]:
        """
        Retrieve student grades by their email and module.
        """
        print(f"Buscando: email='{email}', module='{module}'")
        student_grades = self.collection.find_one({"email": email.strip(), "module": module.strip()})
        print(f"Resultado: {student_grades}")
        if student_grades:
            student_grades["_id"] = str(student_grades["_id"])  # Convertimos el ObjectId a string
        return student_grades

    def list_grades(self) -> list:
        """
        List all grades in the database.
        """
        grades = list(self.collection.find())
        return [{**grade, "_id": str(grade["_id"])} for grade in grades]
