Image-Upload Project README
Introduction

Welcome to the Image-Upload project! This guide will walk you through the steps to set up and run the project using Docker. The project is built using Django and django_rest_framework, and it leverages various libraries and tools to make the development and deployment process seamless.
Technologies Used

    Programming Language: Python
    Frameworks: Django, django_rest_framework
    Libraries: psycopg2, Pillow
    Documentation: drf-spectacular
    Database: PostgreSQL
    Linting: Flake8
    Version Control: Git
    Containerization: Docker
    CI/CD: GitHub Actions

Getting Started

Follow these steps to get the project up and running on your local machine:
1. Clone the Repository

Open your terminal and run the following command to clone the project repository:

git clone https://github.com/Andrew-Kole/image-upload.git

2. Set Up Environment Variables

Copy the .env file from the email attachment to the root of the project. This file contains sensitive data.
3. Build the Docker Container

Build the Docker container by running the following command:

docker-compose build

This process may take a few minutes.
4. Run the Project

Start the project using Docker with the following command:

docker-compose up

This command will perform several actions:

    Lint tests to ensure code readability.
    Unit tests to identify and fix any project issues.
    Wait for the database to be available, avoiding connectivity issues.
    Apply migrations to apply changes to the project.
    Finally, run the project itself.

5. Access Swagger Documentation

Open your web browser and navigate to http://127.0.0.1:8000/api/docs. Here, you can explore and interact with the project's endpoints.
User Management

To access certain endpoints, you'll need to be authorized. Here's how you can create users:

    Create a User: Use the /user/create endpoint in Swagger. Provide an email and password, then click "Execute." New users are assigned the "Basic" role by default.

    Create a Superuser: To create an admin account, run the following command in the terminal:

    docker-compose run --rm app sh -c "python manage.py createsuperuser"

    You can then access all endpoints in Swagger by visiting http://127.0.0.1/admin.

Useful Commands

    docker-compose up: Start the project.
    docker-compose run --rm app sh -c "python manage.py (command)": Run Django management commands within the Docker container.