from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView
from .forms import NoteForm
from .models import Note


class DashboardView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "core/dashboard.html"
    context_object_name = "notes"

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "core/note_form.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)