## Prerequisites

- Python 3.10+
- Node.js v18+ and npm
- pip and virtualenv

---

## Backend Setup

### 1. Navigate to the backend directory
``` bash
cd backend
```
### 2. Create and activate a virtual environment
``` bash
python -m venv venv
```
# macOS / Linux:
``` bash
source venv/bin/activate
```
# Windows:
``` cmd
venv\Scripts\activate
```
### 3. Install dependencies
``` bash
pip install -r requirements.txt
```
### 4. Apply database migrations
``` bash
python manage.py migrate
```
### 5. Seed the database with initial data
> This step is required before running the server. The seed command populates the database with products, suppliers, and stock data needed for the application to work correctly.

python manage.py seed_db

### 6. Start the development server
python manage.py runserver 8000

The API will be available at http://127.0.0.1:8000

---

## Frontend Setup

### 1. Navigate to the frontend directory
``` bash
cd frontend
```
### 2. Install dependencies
``` bash
npm install
```
### 3. Start the development server
``` bash
npm run dev
```
The app will be available at http://localhost:5173

---

## Available Endpoints

| Endpoint | Description |
|---|---|
| http://127.0.0.1:8000/api/docs/ | Swagger UI (API documentation) |

---

## Quick Start (TL;DR)

# Backend
``` bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_db
python manage.py runserver 8000
```

# Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```