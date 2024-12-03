# Project Setup Guide

## Prerequisites
- Python 3.10+
- pip
- virtualenv
- Redis

## Local Development Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd project
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Redis Setup
Ensure Redis is installed and running on your local machine.
- macOS: `brew install redis && brew services start redis`
- Ubuntu: `sudo apt-get install redis-server && sudo systemctl start redis`
- Windows: Download from Redis official website and follow installation instructions

### 5. Environment Variables
Create a `.env` file in the project root with the following:
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

### 6. Database Migrations
```bash
python manage.py migrate
```

### 7. Celery Configuration
Start Celery worker in a separate terminal:
```bash
celery -A project worker -l info
```

### 8. Run Development Server
```bash
python manage.py runserver
```

## Development Commands
- Activate Virtual Environment: `source .venv/bin/activate`
- Install Packages: `pip install -r requirements.txt`
- Run Tests: `python manage.py test`
- Create Migrations: `python manage.py makemigrations`
- Apply Migrations: `python manage.py migrate`

## Troubleshooting
- Ensure Redis is running before starting Celery
- Check `requirements.txt` for exact package versions
- Verify Python and pip versions match project requirements