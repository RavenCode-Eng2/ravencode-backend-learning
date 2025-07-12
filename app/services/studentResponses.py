# src/services/responses_service.py
from typing import Optional, List
from pymongo.results import InsertOneResult, UpdateResult
from app.models.studentResponses import StudentResponses
from app.DB.database import get_database

class ResponsesService:
    """
    Service for managing student responses in the database.
    Handles all operations related to storing and updating student responses.
    """

    def __init__(self):
        self.db = get_database()
        if self.db is None:
            raise Exception("Could not connect to the database")
        self.collection = self.db["student_responses"]

    def create_responses(self, student_responses: StudentResponses) -> dict:
        """
        Create or update the student's responses in the database.
        If the student already has responses, updates them.
        """
        existing_responses = self.get_responses_by_token(student_responses.email)
        if existing_responses:
            update_data = student_responses.dict(exclude_unset=True)
            result = self.collection.update_one(
                {"email": student_responses.email},
                {"$set": update_data}
            )
            return {"updated_count": result.modified_count}

        result = self.collection.insert_one(student_responses.dict())
        return {"inserted_id": str(result.inserted_id), "message": "Responses created successfully"}

    def get_responses_by_token(self, email: str) -> Optional[dict]:
        """
        Retrieve student responses by their token.
        """
        student_responses = self.collection.find_one({"email": email})
        if student_responses:
            student_responses["_id"] = str(student_responses["_id"])
        return student_responses

    def list_all_responses(self) -> List[dict]:
        """
        List all responses from the database.
        """
        responses = list(self.collection.find())
        return [{**response, "_id": str(response["_id"])} for response in responses]

    def delete_responses_by_email(self, email: str) -> dict:
        """
        Delete all responses for a student by their email.
        """
        email = email.strip()
        result = self.collection.delete_many({"email": email})
        return {
            "message": f"Deleted {result.deleted_count} responses for student with email: {email}",
            "deleted_count": result.deleted_count
        }
