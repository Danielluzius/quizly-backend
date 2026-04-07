from rest_framework import serializers
from quizzes_app.models import Quiz, Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for a single quiz question."""

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for a quiz including its nested questions."""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'video_url', 'created_at', 'updated_at', 'questions']
