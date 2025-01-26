from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from base import models as base_models
from doctor import models as doctor_models


@login_required
def dashboard(request):
    
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = doctor_models.Notification.objects.filter(doctor=doctor)

    context = {

        "appointments": appointments,
        "notifications" : notifications,

    }
    return render( request, "doctor/dashboard.html", context)


@login_required
def appointments(request):
    
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    

    context = {

        "appointments": appointments,
       
    }
    return render( request, "doctor/appointments.html", context)


@login_required
def appointment_detail(request,appointment_id):
    doctor = doctor_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    
    medical_records= base_models.MedicalRecord.objects.filter(appointment=appointment)

    lab_tests = base_models.MedicalRecord.objects.filter(appointment=appointment)

    prescriptions = base_models.MedicalRecord.objects.filter(appointment=appointment)

    context = {
        "appointment":appointment,
        "medical_records":medical_records,             
        "lab_tests":lab_tests,
        "prescriptions":prescriptions

    }
    return render (request, "doctor/appointment_detail.html", context)