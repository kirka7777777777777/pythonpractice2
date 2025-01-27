from django.contrib import admin
from .models import Question, Choice
from .models import Category, Application # Импортируйте модель Category и Application


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)

admin.site.register(Category)
admin.site.register(Application)