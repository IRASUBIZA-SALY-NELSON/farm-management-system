from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FarmerForm
from .models import Farmer, Attendance
from django.utils import timezone
from datetime import datetime
from django.db.models import Q


def add_farmer(request):
    if request.method == 'POST':
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farmer saved successfully.')
            return redirect('add_farmer')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmerForm()
    return render(request, 'attendance/add_farmer.html', {'form': form})


def attendance_list(request):
    """List all farmers and allow marking attendance for a given date."""
    # Determine selected date from POST or GET, default to today
    date_str = request.POST.get('attendance_date') or request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
            messages.error(request, 'Invalid date format. Showing attendance for today.')
    else:
        selected_date = timezone.now().date()

    farmers = Farmer.objects.all()

    if request.method == 'POST':
        # Save attendance states for each farmer
        for farmer in farmers:
            is_present = request.POST.get(f'present_{farmer.id}') == 'on'
            Attendance.objects.update_or_create(
                date=selected_date,
                farmer=farmer,
                defaults={'is_present': is_present},
            )
        messages.success(request, 'Attendance saved successfully.')
        return redirect(f"{request.path}?date={selected_date.isoformat()}")

    # Fetch attendance for selected date
    attendance_qs = Attendance.objects.filter(date=selected_date, farmer__in=farmers)
    present_ids = list(attendance_qs.filter(is_present=True).values_list('farmer_id', flat=True))

    context = {
        'farmers': farmers,
        'selected_date': selected_date,
        'present_ids': present_ids,
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
    context = {
        'farmers': farmers,
        'query': query,
    }
    return render(request, 'attendance/farmers_list.html', context)