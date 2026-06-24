from django.urls import path
from .views import DashboardView, NoteCreateView, NoteDeleteView

app_name = "core"
urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("nueva/", NoteCreateView.as_view(), name="note_create"),
    path("eliminar/<int:pk>/", NoteDeleteView.as_view(), name="note_delete"),
]