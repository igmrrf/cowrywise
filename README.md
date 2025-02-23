# Library Management System

This project is a backend assessment task to develop an application that manages books in a library. The system consists of two independent API services: the **Frontend API** for users and the **Backend/Admin API** for administrators.

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

