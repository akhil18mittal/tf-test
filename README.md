## Overview

This project is a Django application that scrapes loan data from a website and saves it to a PostgreSQL database. 
It uses Django Rest Framework (DRF) to provide API endpoints for the Loan, Country, and Sector data. 
The project employs Docker for containerization, and it utilizes Redis, Celery, and Celery Beat for background tasks.
Moreover, Selenium is used for web scraping purposes.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose

## Installation

1. Clone the repository:

2. Navigate to the project folder:

3. Create a .env file with the following variables:

POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>

Replace <your_postgres_user> and <your_postgres_password> with your own PostgreSQL user and password.

4. Build and start the Docker containers:

docker-compose up --build

The application should now be running, and you can access the API endpoints at http://localhost:8000/api/.

API Endpoints

- Loans: http://localhost:8000/api/loans/
- Countries: http://localhost:8000/api/countries/
- Sectors: http://localhost:8000/api/sectors/

Technologies Used

- Docker
- Django Rest Framework (DRF)
- Redis
- Celery
- Celery Beat
- Selenium
