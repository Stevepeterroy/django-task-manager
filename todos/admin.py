from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'priority', 'due_date')
    list_filter = ('completed', 'priority', 'user')
    search_fields = ('title', 'description')
    list_editable = ('completed', 'priority', 'due_date')
    date_hierarchy = 'due_date'