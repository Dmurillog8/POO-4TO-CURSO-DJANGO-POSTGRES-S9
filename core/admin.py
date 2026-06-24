from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at")
    list_filter = ("owner",)
    search_fields = ("title", "body", "owner__username")