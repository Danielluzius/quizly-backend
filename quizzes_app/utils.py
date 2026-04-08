import os
import re
import json
import tempfile
import yt_dlp
import whisper
from google import genai
from quizzes_app.models import Quiz, Question


def extract_video_id(url):
    """Extract the YouTube video ID from any valid YouTube URL format."""
    pattern = r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})'
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f'Could not extract video ID from URL: {url}')
    return match.group(1)


_BROWSERS = ['chrome', 'firefox', 'edge', 'safari', 'opera', 'brave']


def download_audio(url):
    """Download audio from a YouTube URL and return the temp file path.

    Tries without cookies first, then retries with each installed browser's
    cookies until one succeeds.
    """
    video_id = extract_video_id(url)
    tmp_filename = os.path.join(tempfile.gettempdir(), f'{video_id}.%(ext)s')

    base_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_filename,
        'quiet': True,
        'noplaylist': True,
    }

    attempts = [{}] + [{'cookiesfrombrowser': (browser,)} for browser in _BROWSERS]
    last_error = None

    for extra in attempts:
        try:
            ydl_opts = {**base_opts, **extra}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                ext = info.get('ext', 'webm')
            return os.path.join(tempfile.gettempdir(), f'{video_id}.{ext}')
        except yt_dlp.utils.DownloadError as e:
            last_error = e
            continue

    raise last_error


def transcribe_audio(file_path):
    """Transcribe an audio file using Whisper AI and return the transcript string."""
    model = whisper.load_model('base')
    result = model.transcribe(file_path)
    return result['text']


_QUIZ_PROMPT_TEMPLATE = (
    'Based on the following transcript, generate a quiz in valid JSON format.\n\n'
    'The quiz must follow this exact structure:\n'
    '{{\n'
    '  "title": "Create a concise quiz title based on the topic of the transcript.",\n'
    '  "description": "Summarize the transcript in no more than 150 characters.'
    ' Do not include any quiz questions or answers.",\n'
    '  "questions": [\n'
    '    {{\n'
    '      "question_title": "The question goes here.",\n'
    '      "question_options": ["Option A", "Option B", "Option C", "Option D"],\n'
    '      "answer": "The correct answer from the above options"\n'
    '    }},\n'
    '    ...\n'
    '    (exactly 10 questions)\n'
    '  ]\n'
    '}}\n\n'
    'Requirements:\n'
    '- Each question must have exactly 4 distinct answer options.\n'
    '- Only one correct answer is allowed per question, and it must be present in question_options.\n'
    "- The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).\n"
    '- Do not include explanations, comments, or any text outside the JSON.\n\n'
    'Transcript:\n{transcript}'
)


def build_quiz_prompt(transcript):
    """Build and return the Gemini prompt string for quiz generation."""
    return _QUIZ_PROMPT_TEMPLATE.format(transcript=transcript)


def generate_quiz(transcript):
    """Send transcript to Gemini and return parsed quiz data as a dict."""
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=build_quiz_prompt(transcript),
        config=genai.types.GenerateContentConfig(
            response_mime_type='application/json',
        ),
    )
    return json.loads(response.text)


def create_questions(quiz, questions_data):
    """Create Question objects in the database for the given quiz."""
    for q in questions_data:
        Question.objects.create(
            quiz=quiz,
            question_title=q['question_title'],
            question_options=q['question_options'],
            answer=q['answer'],
        )


def save_quiz(data, user, url):
    """Persist the generated quiz and its questions to the database."""
    video_id = extract_video_id(url)
    canonical_url = f'https://www.youtube.com/watch?v={video_id}'
    quiz = Quiz.objects.create(
        user=user,
        title=data['title'],
        description=data.get('description', ''),
        video_url=canonical_url,
    )
    create_questions(quiz, data['questions'])
    return quiz
