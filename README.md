# Learning Platform Evaluation Service

A FastAPI-based evaluation service for a learning platform that manages courses, modules, lessons, assessments, and student progress evaluation.

## Features

- Course Management
  - CRUD operations for courses, modules, lessons, and assessments
  - Content ordering and sequencing
  - Status management (draft/published/archived)

- Progress Tracking
  - User progress through courses and modules
  - Time spent tracking
  - Completion status

- Assessment System
  - Multiple assessment types (coding, quiz, project)
  - Student grade evaluation and tracking
  - Module access control based on assessment results

- Authentication & Authorization
  - JWT-based authentication with user management service
  - Role-based access control (admin, instructor, student)
  - Public key validation from user management service

- Performance Optimization
  - Redis caching for frequently accessed content
  - Pagination support
  - Efficient MongoDB queries

## Architecture

The application follows a clean architecture pattern:

- `app/models/` - Pydantic models for data validation
- `app/services/` - Business logic layer
- `app/api/` - FastAPI route handlers
- `app/core/` - Core functionality (auth, config, cache)
- `app/DB/` - Database connection and configuration

## Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Redis 6.0+
- Access to user management service (for JWT public key)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd learning-platform-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=RavenCodeLearning
JWT_PUBLIC_KEY=your-public-key
JWT_ALGORITHM=RS256
USER_MANAGEMENT_SERVICE_URL=http://localhost:8001
REDIS_URL=redis://localhost:6379
REDIS_CACHE_TTL=3600
API_PORT=8002
```

## Running the Application

1. Start MongoDB and Redis servers

2. Run the application:
```bash
uvicorn app.main:app --reload --port 8002
```

3. Access the API documentation:
- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

## API Endpoints

### Authentication
- All endpoints require a valid JWT token
- Token must be signed by the auth service
- Include token in Authorization header: `Bearer <token>`

### Courses
- `GET /courses` - List courses
- `POST /courses` - Create course
- `GET /courses/{course_id}` - Get course details
- `PUT /courses/{course_id}` - Update course
- `DELETE /courses/{course_id}` - Delete course

### Modules
- `GET /modules` - List modules
- `POST /modules` - Create module
- `GET /modules/{module_id}` - Get module details
- `PUT /modules/{module_id}` - Update module
- `DELETE /modules/{module_id}` - Delete module

### Lessons
- `GET /lessons/module/{module_id}` - List module lessons
- `POST /lessons` - Create lesson
- `GET /lessons/{lesson_id}` - Get lesson details
- `PUT /lessons/{lesson_id}` - Update lesson
- `DELETE /lessons/{lesson_id}` - Delete lesson
- `PUT /lessons/{lesson_id}/status` - Update lesson status

### Assessments
- `GET /assessments/module/{module_id}` - List module assessments
- `POST /assessments` - Create assessment
- `GET /assessments/{assessment_id}` - Get assessment details
- `PUT /assessments/{assessment_id}` - Update assessment
- `DELETE /assessments/{assessment_id}` - Delete assessment
- `PUT /assessments/{assessment_id}/status` - Update assessment status

### Progress
- `GET /progress/courses` - List user's course progress
- `GET /progress/courses/{course_id}` - Get course progress
- `POST /progress/courses/{course_id}/modules/{module_id}/content/{content_id}` - Update content progress

## Caching

The application uses Redis for caching:

- Course content and metadata
- Lesson content
- Assessment content (excluding submissions)
- User progress summaries

Cache invalidation occurs when:
- Content is updated or deleted
- Status changes
- Order changes

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
pytest
```

3. Run linting:
```bash
flake8
```

## Integration with Evaluation Service

The assessment system integrates with an external evaluation service:

1. Assessment content is stored in this service
2. Evaluation service handles:
   - Code execution
   - Test case validation
   - Quiz grading
   - Project evaluation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[License Type] - See LICENSE file for details
