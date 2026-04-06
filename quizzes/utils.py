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


def download_audio(url):
    """Download audio from a YouTube URL and return the temp file path."""
    video_id = extract_video_id(url)
    tmp_filename = os.path.join(tempfile.gettempdir(), f'{video_id}.%(ext)s')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_filename,
        'quiet': True,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info.get('ext', 'webm')
    return os.path.join(tempfile.gettempdir(), f'{video_id}.{ext}')
