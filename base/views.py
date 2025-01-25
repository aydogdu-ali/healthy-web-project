from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

import stripe
from base import models as base_models
from doctor import models as doctor_models
from patient import models as patient_models



# Create your views here.
def index(request):
    services = base_models.Service.objects.all()

    context =  {
        "services": services
    }
    return render(request, "base/index.html", context)


def service_detail(request, service_id):
    service = base_models.Service.objects.get(id=service_id)

    context =  {
        "service": service
    }
    return render(request, "base/service_detail.html", {"service":service})


@login_required
def book_appointment(request, service_id, doctor_id):

    service = base_models.Service.objects.get(id=service_id)
    doctor = doctor_models.Doctor.objects.get(id=doctor_id)
    patient = patient_models.Patient.objects.get(user= request.user)

    if request.method =="POST":
        full_name= request.POST.get("full_name")
        email= request.POST.get("email")
        mobile= request.POST.get("mobile")
        gender= request.POST.get("gender")
        adress= request.POST.get("adress")
        dob= request.POST.get("dob")
        issues= request.POST.get("issues")
        symptoms= request.POST.get("symptoms")


    #update patient bio data
        patient.full_name =full_name
        patient.email=email
        patient.mobile=mobile
        patient.gender=gender
        patient.adress=adress
        patient.dob= dob
        patient.save()

    #create appoinment object
        appoinment= base_models.Appointment.objects.create(
        service=service,
        doctor=doctor,
        patient = patient,
        appointment_date= doctor.next_available_appointment_date,
        issues=issues,
        symptoms=symptoms,
    )


    #create a billing object
        billing = base_models.Billing()
        billing.patient =patient
        billing.appointment=appoinment
        billing.sub_total=appoinment.service.cost
        billing.tax=appoinment.service.cost*18/100
        billing.total = billing.sub_total+billing.tax
        billing.status="unpaid"
        billing.save()

        return redirect("base:checkout",billing.billing_id)

    context =  {
        "service": service,
        "doctor": doctor,
        "patient": patient,
    }
    return render(request, "base/book_appointment.html", context)

# sadece giriş yapan user burayı göremesi için
@login_required
def checkout(request,billing_id):
    billing= base_models.Billing.objects.get(billing_id=billing_id)
    
    context = {

         "billing":billing,
         "stripe_public_key":settings.STRIPE_PUBLIC_KEY,
         "paypal_client_id":settings.PAYPAL_CLIENT_ID,

     }
    return render(request, "base/checkout.html", context)


@csrf_exempt
def stripe_payment(request, billing_id):
    billing= base_models.Billing.objects.get(billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
