Employee Directory Microservice

This microservice provides an API for managing and searching an employee directory for a company. It has been developed based on Python source files, Docker configurations, and requirements, focusing on multi-tenancy, custom rate-limiting, and data security.


Features

Employee Management: Core API for searching employee records.

Organization Isolation: Employee data is strictly segregated by organization, preventing cross-organization data leaks.

Employee Search: Search employees by various attributes (first name, last name, email, position).

Custom Rate Limiting: A basic, in-memory rate-limiting system to prevent API abuse, configurable per organization.

Containerized: Dockerfile and Docker Compose setup for easy deployment and local development.

Unit Tested: Comprehensive unit tests covering API functionality, rate limiting, and data isolation.




Getting Started

Ensure you have the following installed on your Unix-like environment (macOS/Linux):

* Python 3.9+
* pip (Python package installer)
* Docker and Docker Compose

Local Development Setup

1.  Clone the repository:

    git clone https://github.com/arbazpatel/employee-search-microservice.git
    cd employee-search-microservice
    

2.  Create a virtual environment (recommended):
    
    python3 -m venv venv
    source venv/bin/activate
    

3.  Install dependencies:
    
    pip install -r requirements.txt
    

4.  Run the application locally (without Docker):
    
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    The API will be accessible at "http://127.0.0.1:8000".

Running with Docker Compose

Docker Compose simplifies building and running the API and its tests as defined in "docker-compose.yml".

1.  Build and run the services:
    Navigate to the root of the directory (where "docker-compose.yml" is located).
    
    docker compose up --build -d

    The API will be accessible at "http://localhost:8000".

2.  Stop and remove the containers (optional):
    
    docker compose down
    

API Documentation (OpenAPI/Swagger UI)

Once the application is running (either locally or via Docker Compose), you can access the interactive API documentation (Swagger UI) at:

* "http://127.0.0.1:8000/docs" (for local development)
* "http://localhost:8000/docs" (if running via Docker Compose)

This interface allows you to explore all available endpoints, their expected inputs, and example responses.

Running Tests

Tests are integrated into the "docker-compose.yml" setup.

1.  Run tests via Docker Compose:
    
    docker compose run --rm tests
    
    "run": Executes a one-off command in a service.
    "--rm": Removes the container after it exits.

    This command will build the "tests" service image (if not already built) and then execute "pytest tests/" inside it. You will see the test results directly in your terminal.

2.  Run tests locally (if "uvicorn" is not running):
    
    source venv/bin/activate
    pytest tests/
    

Key Architectural Aspects

Multi-Tenancy and Data Isolation

The system supports multiple organizations (tenants), each with its own segregated employee data. Access is controlled via an "X-API-Key" header. Crucially, the system dynamically filters which employee attributes are returned based on each organization's configured "display_columns" (defined in "app/core/config.py"), preventing unauthorized data exposure.

Custom Rate Limiting

A custom, in-memory rate-limiting mechanism is implemented ("app/core/security.py"). It tracks requests per API key within a sliding time window. Each organization can have its own "rate_limit_requests" and "rate_limit_seconds" defined in "app/core/config.py". Requests exceeding the limit receive a "429 Too Many Requests" response.

API Design (FastAPI)

FastAPI is used for building the RESTful API. It leverages Pydantic for robust data validation and serialization, ensuring clear API schemas and automatic OpenAPI documentation generation. API logic is modularized using "APIRouter".

Containerization

The application is containerized using a multi-stage "Dockerfile" to create small, efficient images. "docker-compose.yml" orchestrates the API service and a dedicated test runner, simplifying development, testing, and deployment workflows.

Assumptions and Limitations

In-Memory Database: The employee data is stored in simple Python dictionaries ("app/db/in_memory_db.py"). This means all data is non-persistent and will be lost if the application or container restarts. This was a deliberate choice to meet the assignment's focus on API logic over database setup.

Basic Rate Limiting: The custom rate limiter is in-memory and not distributed. It is suitable for a single-instance deployment but would require a distributed caching solution (e.g., Redis) for horizontally scaled production environments.

No Advanced Authentication/Authorization: Authentication is based on simple API keys. There is no user-level authentication, role-based access control, or token-based authentication (e.g., JWT).

Error Handling: Basic HTTP exceptions are raised for errors. A production system might require more detailed or standardized error responses.

No Database Migrations/ORM: As specified in the requirements, there are no database migration tools or a full Object-Relational Mapper (ORM) integrated.
