import os
import re
import json
import tempfile
import yt_dlp
import whisper
from google import genai
from .models import Quiz, Question


def extract_video_id(url):
    """Extract the YouTube video ID from any valid YouTube URL format."""
    pattern = r'(?:v=|youtu\.be/|embed/|shorts/)([A-Za-z0-9_-]{11})'
    match = re.search(pattern, url)
    if not match:
        raise ValueError(f'Could not extract video ID from URL: {url}')
    return match.group(1)
