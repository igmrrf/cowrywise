# Library Management System

This project is a backend assessment task to develop an application that manages books in a library. The system consists of two independent API services: the **Frontend API** for users and the **Backend/Admin API** for administrators.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for production deployment)
- pip (Python package manager)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/igmrrf/cowrywise
cd cowrywise
```
2. Set up Frontend API:
```bash
cd frontend_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --port=5000
```
3. Set up Backend API (in a new terminal):
```bash
cd backend_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run --port=5001
```
The services will be available at:

- Frontend API: http://localhost:5000
- Backend API: http://localhost:5001


## Production Deployment

### Using Docker Compose

1. Build and start the containers:
```bash
docker-compose up --build
```
This will start:

- Frontend API on port 5000
- Backend API on port 5001

2. Stopping the services:
```bash
docker-compose down
```

### Manual Docker Deployment

1. Build and run Frontend API:
```bash
cd frontend_api
docker build -t library-frontend .
docker run -d -p 5000:5000 library-frontend
```
2. Build and run Backend API:
```bash
cd backend_api
docker build -t library-backend .
docker run -d -p 5001:5001 library-backend
```

### Testing:
Run tests for each service

1. Frontend API tests
```bash
cd frontend_api
python -m pytest
```

2. Backend API tests
```bash
cd backend_api
python -m pytest
```

## Features

### Frontend API (User-Facing)
- Enroll users using email, first name, and last name.
- List all available books.
- Retrieve a single book by its ID.
- Filter books by:
  - Publisher (e.g., Wiley, Apress, Manning)
  - Category (e.g., Fiction, Technology, Science)
- Borrow books by ID (specifying the duration in days).

### Backend/Admin API (Admin-Facing)
- Add new books to the catalogue.
- Remove books from the catalogue.
- List enrolled users.
- List users and their borrowed books.
- List books currently unavailable for borrowing (including availability date).

## Requirements
- Endpoints do **not** require authentication.
- Can be implemented using any Python framework.
- Flexible model design.
- Borrowed books should be marked as unavailable.
- The two services must use **different data stores**.
- Implement a mechanism for **synchronizing changes** between the two services (e.g., when a book is added via the Admin API, it should reflect in the Frontend API).
- Deployment using **Docker containers**.
- Include **unit and integration tests**.

## Deployment
- Use **Docker** to containerize both services.
- Define separate containers for the **Frontend API** and **Admin API**.
- Implement a communication strategy between the two services (e.g., message queues, webhooks, database triggers).

## Testing
- Ensure unit and integration tests are included.
- Cover core functionalities like user enrollment, book borrowing, book addition, and synchronization between services.

---
This project demonstrates an understanding of microservice architecture, inter-service communication, and API development best practices.

