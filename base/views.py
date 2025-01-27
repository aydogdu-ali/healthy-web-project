from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.http import JsonResponse

import requests
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
        billing.status="Unpaid"
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
         "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
         "paypal_client_id":settings.PAYPAL_CLIENT_ID,

     }
    return render(request, "base/checkout.html", context)


@csrf_exempt
def stripe_payment(request, billing_id):
    billing= base_models.Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session =stripe.checkout.Session.create(
        customer_email=billing.patient.email,
        payment_method_types= ['card'],
         line_items = [
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': billing.patient.full_name
                    },
                    'unit_amount': int(billing.total * 100)
                },
                'quantity': 1
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing.billing_id])) + "?session_id={CHECKOUT_SESSION_ID}"
    )

    return JsonResponse({"sessionId": checkout_session.id})
        
def stripe_payment_verify(request, billing_id):
    billing= base_models.Billing.objects.get(billing_id=billing_id)
    session_id= request.GET.get("session_id")
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status =="paid":
        if billing.status =="Unpaid":
            billing.status= "Paid"
            billing.save()
            billing.appointment.status =="completed" # büyük harf olabilir
            billing.appointment.save()

            doctor_models.Notification.objects.create(
                doctor= billing.appointment.doctor,
                appointment=billing.appointment,
                type= "New Appointment"

            )


            patient_models.Notification.objects.create(
                patient= billing.appointment.patient,
                appointment=billing.appointment,
                type= "Appointment Scheduled"

            )
    
            return redirect( f"/payment_status/{billing.billing_id}/?payment_status=paid")
    else:
        return redirect( f"/payment_status/{billing.billing_id}/?payment_status=failed")
    

def get_paypal_access_token():
    token_url ="https://api-m.sandbox.paypal.com/v2/oauth2/token"
    data= {'grant_type':'client_credentials'}
    auth = (settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET_ID)
    response = requests.post(token_url,data= data, auth = auth)

    if response.status_code == 200:
        print("Access Token:", response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get access token from Paypal.Status code: {response.status_code}")

def paypal_payment_verify(reguest, billing_id):
    billing= base_models.Billing.objects.get(billing_id=billing_id)

    transaction_id = reguest.GET.get(transaction_id)
    paypal_api_url = f"htpps://api-m.sanbox.paypal.com./v2/checkout/orders/{transaction_id}"
    headers = {
        "Content-Type": 'application/json',
        "Authorization": f"Bearer{get_paypal_access_token()}"
    }
    response = requests.get(paypal_api_url, headers=headers)

    if response.status.code== 200:
        paypal_order_data = response.json()
        paypal_payment_status = paypal_order_data['status']

        if paypal_payment_status== "COMPLETED":
            if billing.status =="Unpaid":
                billing.status= "Paid"
                billing.save()
                billing.appointment.status =="Completed"
                billing.appointment.save()

            doctor_models.Notification.objects.create(
                doctor= billing.appointment.doctor,
                appointment=billing.appointment,
                type= "New Appointment"

            )


            patient_models.Notification.objects.create(
                patient= billing.appointment.patient,
                appointment=billing.appointment,
                type= "Appointment Scheduled"

            )
    
            return redirect( f"/payment_status/{billing.billing_id}/?payment_status=paid")

        return redirect( f"/payment_status/{billing.billing_id}/?payment_status=failed")  
    return redirect( f"/payment_status/{billing.billing_id}/?payment_status=failed") 
    
 



@login_required
def payment_status(request, billing_id):
    billing= base_models.Billing.objects.get(billing_id=billing_id)
    payment_status= request.GET.get("payment_status")

    context = {

        "billing":billing,
        "payment_status":payment_status,
    }

    return render(request, "base/payment_status.html", context)