from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ("title", "body")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título"}),
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "Contenido", "rows": 3}),
        }