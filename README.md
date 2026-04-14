# SmartMarket

A web-based solution for smart warehouse management, predictive restocking, and expiration date monitoring. Built with Django (Backend) and React (Frontend).

## Project Structure
- `/backend` - Django REST Framework API
- `/frontend` - React.js + Vite

---

## Prerequisites
- **Python 3.10+**
- **Node.js (v18+)** & **npm**
- **Virtualenv** (`pip install virtualenv`)

---

## Backend Setup (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: If requirements.txt is missing, install manually: `pip install django djangorestframework django-cors-headers`*

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Run the server:**
   ```bash
   python manage.py runserver 8000
   ```

---

## Frontend Setup (React)

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   *The app will be available at http://localhost:5173*

---

## API Endpoints
- Admin Panel: `http://127.0.0.1:8000/admin/`
- API Root: `http://127.0.0.1:8000/api/`
