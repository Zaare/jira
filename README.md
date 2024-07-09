# Jira Task Management System

This project is a simplified and limited version of Jira, implemented using Django, Django REST Framework (DRF), and Celery. It allows users to manage tasks within an organization. Users can create, view, update, and delete tasks, which have attributes such as title, description, due date, priority level, and status.

## Features

- **Task Management**: Users can create, view, update, and delete tasks.
- **Organizations**: Multiple organizations can join the system. Each organization can have its own administrators and developers.
- **Role-Based Access Control**:
  - **Organizations**: Can manage their members and have full control over their own data.
  - **Administrators**: Can manage members within their organization but cannot modify other administrators' access. They have CRUD operations on sprints and tasks.
  - **Developers**: Can update task statuses but cannot delete tasks or control other users' access.
- **Task Statuses**: Tasks can have statuses such as To Develop, Developing, To Review, Approved, To Test, Delivered.
- **Sprint Management**: Basic Jira concepts such as Backlog, Active Sprint, Future Sprints, and Comments are included.
- **Mentioning Users**: Users can mention each other in tasks and comments.
- **Asynchronous Task Processing**: Celery is used for asynchronous task processing, e.g., sending email notifications when a task is marked as completed (mocked but can be implemented for real email sending).

## Technologies Used

- **PostgreSQL**: Database
- **Redis**: In-memory data structure store for Celery
- **Celery**: Asynchronous task queue/job queue
- **Django**: Web framework
- **Django REST Framework (DRF)**: Toolkit for building Web APIs

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Zaare/jira.git
    cd jira
    ```

2. Build and run the Docker containers:
    ```bash
    docker compose build
    docker compose up
    ```

3. **Optional**: Users can log in to view the project at `localhost:8000` using the username `admin` and password `admin`.

## Testing

Run the tests in the web container to ensure everything is working:
```bash
pytest
```

---

Feel free to adjust any details as necessary!