from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDate
from .models import Note
from django.db.models import Q 
from datetime import datetime

def index(request):
    query = request.GET.get('q', '')  # Search query
    date_str = request.GET.get('date', '')  # Date filter from calendar

    notes = Note.objects.all()

    # Filter by search query if present
    if query:
        notes = notes.filter(
            Q(heading__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by task_date if present and valid
    if date_str:
        try:
            # Parse the date string safely
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            notes = notes.filter(task_date=date_obj)
        except ValueError:
            # If date parsing fails, return all notes or handle as needed
            notes = Note.objects.all()

    context = {
        'notes': notes,
        'query': query,
        'selected_date': date_str,
    }
    return render(request, 'notes/index.html', context)


def add_note(request):
    if request.method == "POST":
        heading = request.POST.get("heading")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        task_date_str = request.POST.get("task_date")

        if heading and description and priority:
            note = Note(
                heading=heading,
                description=description,
                priority=priority
            )

            if task_date_str:
                try:
                    note.task_date = datetime.strptime(task_date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass  # Invalid date, ignore

            note.save()
        return redirect("index")


def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        heading = request.POST.get("heading")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        task_date_str = request.POST.get("task_date")

        if heading and description and priority:
            note.heading = heading
            note.description = description
            note.priority = priority

            # Handle task_date if provided
            if task_date_str:
                try:
                    # Convert string to date object
                    note.task_date = datetime.strptime(task_date_str, "%Y-%m-%d").date()
                except ValueError:
                    # Handle invalid date format if needed
                    pass
            else:
                note.task_date = None  # or keep existing date if you prefer

            note.save()
            return redirect("index")

    return render(request, "notes/edit_note.html", {"note": note})


def delete_note(request, note_id):
    Note.objects.filter(id=note_id).delete()
    return redirect("index")
