from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    """Inline editor for questions within the quiz admin view."""

    model = Question
    extra = 0


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Admin configuration for the Quiz model."""

    list_display = ['title', 'user', 'created_at']
    inlines = [QuestionInline]
