from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Inline editor for questions within the quiz admin view."""

    model = Question
    extra = 0
    fields = ['question_title', 'question_options', 'answer']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin configuration for the Quiz model."""

    list_display = ['title', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['video_url', 'created_at', 'updated_at']
    inlines = [QuestionInline]
