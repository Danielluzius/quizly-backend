# Quizly Backend

🌐 Sprache: [English](README.md) | **Deutsch**

Django REST API, die aus YouTube-Videos automatisch Quizze erstellt – mithilfe von Whisper AI und Gemini.

## Pipeline

YouTube-URL → yt-dlp (Audio) → FFMPEG → Whisper AI (Transkription) → Gemini Flash (Quiz-Generierung) → DB

## Voraussetzungen

- Python 3.10+
- **FFMPEG muss global installiert sein** (wird von Whisper benötigt):
  ```
  winget install ffmpeg
  ```
- **yt-dlp** wird für den YouTube-Audio-Download verwendet und wird automatisch über `requirements.txt` installiert

## Setup

1. Repository klonen:

   ```bash
   git clone https://github.com/Danielluzius/quizly-backend.git
   cd quizly-backend
   ```

2. Virtuelle Umgebung erstellen und aktivieren:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Abhängigkeiten installieren:

   ```bash
   pip install -r requirements.txt
   ```

4. `.env`-Datei auf Basis von `.env.example` erstellen:

   ```
   SECRET_KEY="dein-django-secret-key"
   GEMINI_API_KEY="dein-gemini-api-key"
   ```

   Einen Gemini API-Key erhältst du unter: https://aistudio.google.com

5. Migrationen ausführen:

   ```bash
   python manage.py migrate
   ```

6. Admin-Benutzer erstellen (optional, für das Django Admin-Panel unter `/admin/`):
   ```bash
   python manage.py createsuperuser
   ```

7. Entwicklungsserver starten:
   ```bash
   python manage.py runserver
   ```

Die API ist dann erreichbar unter: `http://127.0.0.1:8000/api/`

## API-Endpunkte

| Methode | Endpunkt              | Beschreibung                     | Auth   |
| ------- | --------------------- | -------------------------------- | ------ |
| POST    | `/api/register/`      | Neuen Benutzer registrieren      | Nein   |
| POST    | `/api/login/`         | Anmelden, setzt JWT-Cookies      | Nein   |
| POST    | `/api/logout/`        | Abmelden, löscht Cookies         | Ja     |
| POST    | `/api/token/refresh/` | Access-Token erneuern            | Cookie |
| POST    | `/api/quizzes/`       | Quiz aus YouTube-URL generieren  | Ja     |
| GET     | `/api/quizzes/`       | Alle eigenen Quizze abrufen      | Ja     |
| GET     | `/api/quizzes/{id}/`  | Einzelnes Quiz abrufen           | Ja     |
| PATCH   | `/api/quizzes/{id}/`  | Titel/Beschreibung aktualisieren | Ja     |
| DELETE  | `/api/quizzes/{id}/`  | Quiz löschen                     | Ja     |

## Frontend

```bash
git clone https://github.com/Developer-Akademie-Backendkurs/project.Quizly frontend
```

Mit Live Server in VS Code öffnen. Das Frontend erwartet das Backend unter `http://127.0.0.1:8000`.
