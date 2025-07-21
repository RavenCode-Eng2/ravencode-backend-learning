from typing import List, Dict, Any, Optional
from .studentGrades import GradesService
from .courses.course_service import CourseService
from .modules.module_service import ModuleService

class ModuleAccessService:
    """
    Service for evaluating student access to modules based on grades and prerequisites.
    """
    
    def __init__(self):
        self.grades_service = GradesService()
        self.course_service = CourseService()
        self.module_service = ModuleService()
    
    async def check_module_access(self, student_email: str, course_id: str, module_id: str) -> Dict[str, Any]:
        """
        Check if a student has access to a specific module based on prerequisites and grades.
        
        Args:
            student_email: Student's email address
            course_id: Course ID
            module_id: Module ID to check access for
            
        Returns:
            Dict containing access status and reason
        """
        try:
            # Get the module information
            module = await self.module_service.get_module(module_id)
            if not module:
                return {
                    "has_access": False,
                    "reason": "Module not found",
                    "required_grade": None,
                    "current_grade": None
                }
            
            # Check if module has prerequisites
            prerequisites = getattr(module, 'prerequisites', [])
            
            # If no prerequisites, module is accessible
            if not prerequisites:
                return {
                    "has_access": True,
                    "reason": "No prerequisites required",
                    "required_grade": None,
                    "current_grade": None
                }
            
            # Check each prerequisite
            for prerequisite_module_id in prerequisites:
                prerequisite_access = await self._check_prerequisite_completion(
                    student_email, prerequisite_module_id
                )
                if not prerequisite_access["completed"]:
                    return {
                        "has_access": False,
                        "reason": f"Prerequisite module {prerequisite_module_id} not completed",
                        "required_grade": prerequisite_access["required_grade"],
                        "current_grade": prerequisite_access["current_grade"],
                        "prerequisite_module": prerequisite_module_id
                    }
            
            return {
                "has_access": True,
                "reason": "All prerequisites completed",
                "required_grade": None,
                "current_grade": None
            }
            
        except Exception as e:
            return {
                "has_access": False,
                "reason": f"Error checking access: {str(e)}",
                "required_grade": None,
                "current_grade": None
            }
    
    async def _check_prerequisite_completion(self, student_email: str, module_id: str, passing_grade: float = 40.0) -> Dict[str, Any]:
        """
        Check if a student has completed a prerequisite module with a passing grade.
        
        Args:
            student_email: Student's email address
            module_id: Module ID to check completion for
            passing_grade: Minimum grade required to pass (default: 40.0)
            
        Returns:
            Dict containing completion status and grade information
        """
        try:
            # Get the student's grade for this module
            # Note: We need to map module_id to the assessment name used in grades
            # For now, we'll use a simple mapping based on your frontend structure
            assessment_name = self._get_assessment_name_for_module(module_id)
            
            grade_record = self.grades_service.get_grades_by_token(student_email, assessment_name)
            
            if not grade_record:
                return {
                    "completed": False,
                    "current_grade": None,
                    "required_grade": passing_grade,
                    "reason": "No grade found for prerequisite module"
                }
            
            current_grade = grade_record.get("grade", 0.0)
            
            return {
                "completed": current_grade >= passing_grade,
                "current_grade": current_grade,
                "required_grade": passing_grade,
                "reason": f"Grade: {current_grade}/{passing_grade}"
            }
            
        except Exception as e:
            return {
                "completed": False,
                "current_grade": None,
                "required_grade": passing_grade,
                "reason": f"Error checking prerequisite: {str(e)}"
            }
    
    def _get_assessment_name_for_module(self, module_id: str) -> str:
        """
        Map module ID to assessment name used in the grades system.
        This is a temporary mapping based on your current frontend structure.
        """
        # Based on your frontend, Assessment1 unlocks Module 2
        module_assessment_mapping = {
            "python-module1": "Assessment1",
            "python-module2": "Assessment2",
            "js-module1": "js-assessment1",
            "js-module2": "js-advanced-assessment",
            "java-module1": "java-assessment1",
            "java-module2": "java-advanced-assessment"
        }
        
        return module_assessment_mapping.get(module_id, f"{module_id}-assessment")
    
    async def get_student_module_access_for_course(self, student_email: str, course_id: str) -> Dict[str, Any]:
        """
        Get access status for all modules in a course for a specific student.
        
        Args:
            student_email: Student's email address
            course_id: Course ID
            
        Returns:
            Dict containing access status for each module
        """
        try:
            # Get course with modules
            course = await self.course_service.get_course(course_id)
            if not course:
                return {"error": "Course not found"}
            
            module_access = {}
            
            # For each module in the course
            for module_id in getattr(course, 'module_ids', []):
                access_info = await self.check_module_access(student_email, course_id, module_id)
                module_access[module_id] = access_info
            
            return {
                "course_id": course_id,
                "student_email": student_email,
                "module_access": module_access
            }
            
        except Exception as e:
            return {"error": f"Error getting module access: {str(e)}"}
    
    async def check_python_module2_access(self, student_email: str) -> bool:
        """
        Specific check for Python Module 2 access based on Assessment1 grade.
        This matches your current frontend logic.
        
        Args:
            student_email: Student's email address
            
        Returns:
            Boolean indicating if Module 2 should be unlocked
        """
        try:
            grade_record = self.grades_service.get_grades_by_token(student_email, "Assessment1")
            
            if not grade_record:
                return False
            
            current_grade = grade_record.get("grade", 0.0)
            return current_grade >= 40.0
            
        except Exception:
            return False 