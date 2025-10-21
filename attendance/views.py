from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FarmerForm
from .models import Farmer, Attendance
from django.utils import timezone
from datetime import datetime
from django.db.models import Q


# --- Helpers ---------------------------------------------------------------

def _get_selected_date(request):
    """Parse date from request or fallback to today. Adds a flash on invalid format."""
    date_str = request.POST.get('attendance_date') or request.GET.get('date')
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Showing attendance for today.')
    return timezone.now().date()


def _save_attendance(selected_date, farmers, post_data):
    """Upsert attendance for each farmer given checkbox values in post_data."""
    for farmer in farmers:
        is_present = post_data.get(f'present_{farmer.id}') == 'on'
        Attendance.objects.update_or_create(
            date=selected_date,
            farmer=farmer,
            defaults={'is_present': is_present},
        )


def _present_ids_for_date(selected_date, farmers):
    return list(
        Attendance.objects.filter(
            date=selected_date, farmer__in=farmers, is_present=True
        ).values_list('farmer_id', flat=True)
    )


# --- Views -----------------------------------------------------------------

def add_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer saved successfully.')
            return redirect('add_farmer')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmerForm()
    return render(request, 'attendance/add_farmer.html', {'form': form})


def attendance_list(request):
    selected_date = _get_selected_date(request)
    farmers = Farmer.objects.all()

    if request.method == 'POST':
        _save_attendance(selected_date, farmers, request.POST)
        messages.success(request, 'Attendance saved successfully.')
        return redirect(f"{request.path}?date={selected_date.isoformat()}")

    context = {
        'farmers': farmers,
        'selected_date': selected_date,
        'present_ids': _present_ids_for_date(selected_date, farmers),
    }
    return render(request, 'attendance/attendance_list.html', context)


def farmers_list(request):
    """Simple list of farmers with optional search query."""
    query = request.GET.get('q', '').strip()
    farmers = Farmer.objects.all()
    if query:
        farmers = farmers.filter(
            Q(name__icontains=query) | Q(farm__icontains=query) | Q(location__icontains=query)
        )
    return render(request, 'attendance/farmers_list.html', {'farmers': farmers, 'query': query})