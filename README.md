# Quizly Backend

Django REST API that generates quizzes from YouTube videos using Whisper AI and Gemini.

## Pipeline

YouTube URL → yt-dlp (audio) → FFMPEG → Whisper AI (transcription) → Gemini Flash (quiz generation) → DB

## Requirements

- Python 3.10+
- **FFMPEG must be installed globally** (required by Whisper):
  ```
  winget install ffmpeg
  ```
- **yt-dlp** is used for downloading YouTube audio and is installed automatically via `requirements.txt`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Danielluzius/quizly-backend.git
   cd quizly-backend
   ```

2. Create and activate the virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:

   ```
   SECRET_KEY="your-django-secret-key"
   GEMINI_API_KEY="your-gemini-api-key"
   ```

   Get a Gemini API key at: https://aistudio.google.com

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoints

| Method | Endpoint              | Description                    | Auth   |
| ------ | --------------------- | ------------------------------ | ------ |
| POST   | `/api/register/`      | Register new user              | No     |
| POST   | `/api/login/`         | Login, sets JWT cookies        | No     |
| POST   | `/api/logout/`        | Logout, clears cookies         | Yes    |
| POST   | `/api/token/refresh/` | Refresh access token           | Cookie |
| POST   | `/api/quizzes/`       | Generate quiz from YouTube URL | Yes    |
| GET    | `/api/quizzes/`       | List all user quizzes          | Yes    |
| GET    | `/api/quizzes/{id}/`  | Get a specific quiz            | Yes    |
| PATCH  | `/api/quizzes/{id}/`  | Update title/description       | Yes    |
| DELETE | `/api/quizzes/{id}/`  | Delete a quiz                  | Yes    |

## Frontend

```bash
git clone https://github.com/Developer-Akademie-Backendkurs/project.Quizly frontend
```

Open with Live Server in VS Code. The frontend expects the backend at `http://127.0.0.1:8000`.
