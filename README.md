# SalesGo Django Project

This project is a Django-based web application named **SalesGo**. It is designed to run within a Docker container and includes user authentication, post management, and more.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Steps to Run the Server via Docker

1. **Open Terminal**: Navigate to the SalesGo directory where the `docker-compose.yml` file is located.
   
   ```bash
   cd /path/to/SalesGo

2. Build and Start the Containers: docker-compose up --build

3. Check Container Status: docker ps

4. Access the Container: docker exec -it <container_id> /bin/bash

5. Apply Migrations: python manage.py migrate

6. Collect Static Files incase css did not load correctly: python manage.py collectstatic

### List of URLs in the Project

/login - Login page
/dashboard - Dashboard page
/signup - Sign-up page
/logout - Logout
/posts - List of posts
/post/create/ - Create a post
post/edit/<int:pk> - Update a post
post/delete/<int:pk> - Delete a post

