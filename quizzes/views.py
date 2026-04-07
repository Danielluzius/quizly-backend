from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Quiz
from .serializers import QuizSerializer
from .utils import download_audio, transcribe_audio, generate_quiz, save_quiz
import os


class QuizViewSet(viewsets.ModelViewSet):
    """ViewSet for creating, listing, retrieving, updating and deleting quizzes."""

    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Return only quizzes belonging to the authenticated user, newest first."""
        return Quiz.objects.filter(user=self.request.user).order_by('-created_at')

    def create(self, request):
        """Run the full pipeline: URL → audio → transcript → quiz → DB."""
        url = request.data.get('url', '').strip()
        if not url:
            return Response({'detail': 'URL is required.'}, status=status.HTTP_400_BAD_REQUEST)
        audio_path = download_audio(url)
        try:
            transcript = transcribe_audio(audio_path)
            quiz_data = generate_quiz(transcript)
            quiz = save_quiz(quiz_data, request.user, url)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
        serializer = self.get_serializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Allow updating only title and description."""
        allowed = {k: v for k, v in request.data.items() if k in ('title', 'description')}
        serializer = self.get_serializer(self.get_object(), data=allowed, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
