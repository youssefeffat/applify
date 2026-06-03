# Applify

Applify is a modern web platform built with a **Vue 3 / Vite** frontend and a **Python / FastAPI microservices** backend. 

This repository contains two main directories:
- `/Frontend`: The Vue 3 client application.
- `/Backend`: The Python microservices (Auth Service, User Service, API Gateway, etc.) and database configurations.

---

## 🚀 Getting Started

You can run the Applify project in two ways: using Docker for a quick, containerized setup, or running the services separately for local development and debugging.

### Option 1: Running with Docker (Recommended)

Docker is the easiest way to spin up the entire architecture, including the database, frontend, and all backend microservices.

1. Ensure you have **Docker** and **Docker Compose** installed on your machine.
2. Open a terminal at the root of the project.
3. Build and start the containers:
   ```bash
   docker compose up --build
   ```
4. Once the containers are running, you can access:
   - **Frontend Application**: `http://localhost:5173`
   - **API Gateway (Backend)**: `http://localhost:8000`

*(To stop the application, press `Ctrl+C` or run `docker compose down`)*

---

### Option 2: Running Services Separately (Local Development)

If you are actively developing and want hot-reloading for both the frontend and backend, you can start them separately.

#### 1. Start the Frontend
The frontend uses `pnpm` as its package manager.

```bash
# Navigate to the frontend directory
cd Frontend

# Install dependencies
pnpm install

# Start the development server
pnpm run dev
```
The Vue application will be accessible at `http://localhost:5173`.

#### 2. Start the Backend Microservices
The backend consists of multiple Python services. You will need to start the API Gateway and the individual domain services.

```bash
# Navigate to the backend directory
cd Backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate
# Activate the virtual environment (Mac/Linux)
# source venv/bin/activate

# Install the dependencies
pip install -r requirements.txt

# Setup your environment variables
cp .env.example .env
```

To run the backend, you need to start the API Gateway and the supporting microservices. Open separate terminal tabs for each service:

```bash
# Terminal 1: Start the API Gateway
uvicorn api-gateway.main:app --port 8000 --reload

# Terminal 2: Start the Auth Service
uvicorn auth-service.main:app --port 8001 --reload

# Terminal 3: Start the User Profile Service
uvicorn user-service.main:app --port 8002 --reload
```

---

## ⚙️ Configuration

Before running the application, make sure your database and environment variables are properly configured.
- Check the `Backend/.env.example` file and copy its contents to a `.env` file to configure your PostgreSQL connection and JWT secrets.
- Check the `Frontend` directory for any required `.env` file to configure the base API URL (e.g., `VITE_API_BASE_URL=http://localhost:8000`).
