## Overview

This project is a Django application with PostgreSQL as the database backend. It includes a dynamic employee search API with configurable columns and filters based on the organization.

## Prerequisites

Ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Project Setup

### Using Docker

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Build and Start the Containers**

   ```bash
   docker-compose up --build
   ```

   This will build the Docker images and start the containers for the application and the PostgreSQL database.

3. **Access the Application**

   The application will be available at `http://localhost:8000`.

   For the Swagger API documentation, visit `http://localhost:8000/swagger/`.

### Without Docker

1. **Create a Virtual Environment**

   ```bash
   python -m venv env
   source env/bin/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up the Database**

   Make sure PostgreSQL is running and create a database with the following credentials:

   - **Database Name**: `django_db`
   - **User**: `django_user`
   - **Password**: `django_password`

   Update the `DATABASES` configuration in `settings.py` if necessary.

4. **Run Migrations**

   Run the migrations to set up the database schema:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**

   To create a Django superuser for accessing the admin interface, run:

   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**

   The application will be available at `http://localhost:8000`.

   For the Swagger API documentation, visit `http://localhost:8000/swagger/`.

## API Endpoints

- **Employee Search API**: `/api/employees/`

  This endpoint supports filtering based on status, location, department, and position. The available filters and columns are configurable per organization.

## Development

- **Updating Dependencies**

  If you need to update the dependencies, modify the `requirements.txt` file and run:

  ```bash
  pip install -r requirements.txt
  ```

- **Running Tests**

  To run the unit tests, execute:

  ```bash
  python manage.py test
  ```
This version includes instructions for setting up and running the project using Docker, as well as the traditional method without Docker.
