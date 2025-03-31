![alt text](https://rightshero.com/wp/wp-content/uploads/2024/04/RightsHero-Logo.png)

# Category Checker - Local Setup Guide

## Overview
This project is a category management system that dynamically generates subcategories based on user interactions. The application is built using **Django** and **Docker**, making it easy to set up and run locally.

## Prerequisites
Ensure you have the following installed on your machine:
- **Docker** & **Docker Compose** ([Installation Guide](https://docs.docker.com/get-docker/))
- **Git** ([Installation Guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git))
- **Make** (Optional but recommended for running commands easily)

## Installation Steps

### 1. Clone the Repository
```sh
git clone https://github.com/Omarmoatz/sw_task.git
cd category-checker
```

### 2. Create an `.env` File
Copy the example environment file and modify it as needed:
```sh
cp .env.example .env
```
Ensure that the `.env` file contains the necessary configurations such as database credentials.

### 3. Build and Run the Project
Run the following command to build and start the services using Docker:
```sh
docker-compose up --build -d
```
This will:
- Start the **PostgreSQL** database
- Start the **Django** backend
- Set up all necessary dependencies

### 4. Apply Migrations & Create a Superuser
Run the following commands inside the Django container:
```sh
docker compose run --rm django python manage.py makemigrations
docker compose run --rm django python manage.py migrate
docker compose run --rm django python manage.py createsuperuser
```
Follow the prompts to create an admin user.

### 5. Access the Application
- **Backend API:** `http://localhost:8000/api/docs`
- **Home Page:** `http://localhost:8000` or `http://127.0.0.1:8000` 
- **Admin Panel:** `http://localhost:8000/admin/` (Use the superuser credentials you created)

### 6. Running Tests
To ensure everything is working correctly, run the test suite:
```sh
docker-compose exec web pytest
```

## Stopping the Application
To stop the running containers, use:
```sh
docker-compose down
```

## Troubleshooting
### 1. Checking Logs
If you encounter issues, check the logs with:
```sh
docker-compose logs -f
```
### 2. Restarting the Application
Sometimes, restarting the application resolves issues:
```sh
docker-compose down && docker-compose up --build -d
```

## Contributing
If you'd like to contribute, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

---
For any issues or questions, please open a GitHub issue in the repository.
