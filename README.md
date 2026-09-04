Insurance Management System

A backend Insurance Management System built using FastAPI, SQLAlchemy, SQLite, and Alembic. The application provides APIs for managing customers, insurance plans, policies, claims, claim documents, assessments, beneficiaries, premium payments, settlements, notifications, users, and audit logs.

Project Overview

The Insurance Management System is designed to manage the complete insurance lifecycle through RESTful APIs.

The system supports:

- User management and authentication
- Customer management
- Insurance plan management
- Policy creation and management
- Policy renewal and cancellation
- Beneficiary management
- Premium payment tracking
- Insurance claim management
- Claim document management
- Claim assessment
- Claim approval and rejection
- Settlement management
- Notifications
- Audit logging
- Role-based access control
- Input validation
- Database migrations
- Automated testing

Technology Stack

- Python 3.14+
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- JWT Authentication
- Pytest
- Pytest-Cov
- Uvicorn

Project Structure

insurance-management-system/
│
├── app/
│   ├── core/
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   ├── permissions.py
│   │   └── security.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── insurance_plan.py
│   │   ├── policy.py
│   │   ├── beneficiary.py
│   │   ├── premium_payment.py
│   │   ├── claim.py
│   │   ├── claim_document.py
│   │   ├── claim_assessment.py
│   │   ├── settlement.py
│   │   ├── notification.py
│   │   └── audit_log.py
│   │
│   ├── repositories/
│   │
│   ├── routes/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   ├── utils/
│   │
│   ├── config.py
│   ├── database.py
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│
├── alembic.ini
├── requirements.txt
├── insurance_management.db
└── README.md

Features

Authentication and Authorization

The application uses authentication and role-based authorization to protect API endpoints.

Supported roles include different levels of access for administrators, staff members, claims officers, and customers.

JWT tokens are used for authenticated API access.

Customer Management

The system provides functionality to:

- Create customers
- Retrieve customer details
- Update customer information
- List customers
- Validate customer information

Insurance Plan Management

Insurance plans can be created and managed with information such as:

- Plan name
- Plan type
- Premium
- Coverage amount
- Duration
- Plan status

Policy Management

The policy module supports:

- Creating policies
- Retrieving policies
- Updating policies
- Listing policies
- Policy activation
- Policy cancellation
- Policy renewal
- Policy status validation
- Policy ownership validation

Beneficiary Management

Beneficiaries can be associated with policies and managed through dedicated APIs.

The system validates beneficiary information and policy ownership before performing operations.

Premium Payment Management

The application supports tracking premium payments associated with policies.

Payment information can be created, retrieved, and validated against the corresponding policy.

Claim Management

The claim module manages the complete claim lifecycle.

Supported claim statuses include:

- Submitted
- Under Review
- Documents Required
- Approved
- Rejected
- Settled

Claim functionality includes:

- Creating claims
- Retrieving claims
- Listing claims
- Updating claims
- Submitting claims for review
- Approving claims
- Rejecting claims
- Validating claim amounts
- Validating incident dates
- Preventing updates to finalized claims

Claims can only be created for active policies and are validated against policy coverage and ownership.

Claim Documents

Claim documents can be uploaded and managed as part of the claim verification process.

The system supports document verification before a claim can be approved.

Claim Assessment

Claims officers can perform assessments on claims.

Assessments contain information such as:

- Eligible amount
- Assessment notes
- Recommendation
- Assessor
- Assessment timestamp

Settlement Management

Approved claims can be processed through settlement management.

Settlement functionality includes:

- Creating settlements
- Retrieving settlements
- Updating settlements
- Validating settlement amounts
- Tracking settlement status

Notifications

The application provides notification functionality for important events such as policy and claim status changes.

Audit Logging

Important system actions are recorded using audit logs to provide traceability of operations.

API Documentation

FastAPI automatically provides interactive API documentation.

After starting the application, Swagger UI is available at:

http://127.0.0.1:8000/docs

ReDoc is available at:

http://127.0.0.1:8000/redoc

API Base URL

/api/v1

Example:

http://127.0.0.1:8000/api/v1

Installation

Clone the repository:

git clone <repository-url>

Navigate to the project directory:

cd insurance-management-system

Create a virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\activate

Activate the virtual environment on Linux or macOS:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Environment Configuration

Create a `.env` file if environment-based configuration is required.

Example configuration:

DATABASE_URL=sqlite:///./insurance_management.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Database Setup

The project uses SQLite with SQLAlchemy.

Run the Alembic migrations:

alembic upgrade head

To create a new migration after modifying database models:

alembic revision --autogenerate -m "migration message"

Apply the migration:

alembic upgrade head

Running the Application

Start the FastAPI application using Uvicorn:

uvicorn app.main:app --reload

The application will be available at:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs

Testing

The project uses Pytest for automated testing.

Run all tests:

pytest -q

Run tests with coverage:

pytest --cov=app --cov-report=term-missing

Run tests for a specific module:

pytest -q tests/test_claims.py

Run claim service coverage:

pytest -q tests/test_claims.py --cov=app.services.claim_service --cov-report=term-missing

Test Coverage

The project has extensive automated test coverage across the application.

The claim service has been tested to 100% coverage.

Example:

app\services\claim_service.py    88    0    100%

The test suite covers:

- Successful operations
- Validation failures
- Authentication and authorization
- Invalid status transitions
- Missing resources
- Duplicate records
- Business rule validation
- API routes
- Service layer functionality
- Schema validation
- Error handling

Database Tables

The application contains the following major database tables:

- users
- customers
- insurance_plans
- policies
- beneficiaries
- premium_payments
- claims
- claim_documents
- claim_assessments
- settlements
- notifications
- audit_logs

Error Handling

The application uses FastAPI HTTP exceptions to provide meaningful error responses.

Common HTTP status codes include:

200 OK
Successful request.

201 Created
Resource successfully created.

400 Bad Request
Invalid request or business rule violation.

401 Unauthorized
Authentication is required or authentication failed.

403 Forbidden
The authenticated user does not have permission to perform the operation.

404 Not Found
Requested resource does not exist.

409 Conflict
Request conflicts with an existing resource.

422 Unprocessable Entity
Request validation failed.

Security

Security features implemented in the application include:

- Password hashing
- JWT-based authentication
- Authentication dependencies
- Role-based authorization
- Protected API endpoints
- Request validation
- Business rule validation

Development Workflow

Create and activate the virtual environment:

python -m venv venv
.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run database migrations:

alembic upgrade head

Start the application:

uvicorn app.main:app --reload

Run tests:

pytest -q

Run coverage:

pytest --cov=app --cov-report=term-missing

Git Workflow

Check the current changes:

git status

Add changes:

git add .

Commit changes:

git commit -m "Complete insurance management system assignment"

Push changes:

git push

Important Notes

- Do not commit sensitive `.env` files containing real secrets.
- Do not commit the virtual environment directory.
- Database migrations should be committed along with model changes.
- Run the complete test suite before submitting the assignment.
- Keep API documentation updated when adding or modifying endpoints.

Conclusion

This project implements a complete backend Insurance Management System using FastAPI and SQLAlchemy. It follows a layered architecture with routes, schemas, services, repositories, and database models.

The application includes authentication, authorization, insurance policy management, claims processing, assessments, settlements, notifications, audit logging, database migrations, and comprehensive automated testing.
