from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
#forms.py de register ve login formunu import ediyoruz.
from userauths import forms as userauths_forms
from doctor import models as doctor_models
from patient import models as patient_models
from userauths import models as userauths_models

#kullanıcı yetkili ise ana sayfaya gidecek.
def register_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    if request.method =="POST":
        #form ile kullanıcıyı kaydetme
        form =userauths_form.UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            email = form.cleaned_data.get("email")
            password1 = form.cleaned_data.get("password")
            user_type = form.cleaned_data.get("user_type")

            user = authenticate(request, email=email, password=password1)
            if user is not None:
                login(request,user)
        
        #Kullanıcıyı şeçilen kişiye göre database kaydetme işlemi
            if user_type == "Doctor":
                doctor_models.Doctor.objects.create(user=user, full_name=full_name)
            else:
                patient_models.Patient.objects.create(user=user, full_name=full_name)
            messages.success(request,"Account created successfully")
            return redirect("/")
        else:
            messages.error(request, "Authenticated failed, Please Try Again!")

    
    else:
            form = userauths_forms.UserRegisterForm()

    context = {
        'form':form
    }
    return render(request, "userauths/sign-up.html", context) 



def login_view(request):
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("/")
    
    if request.method =="POST":
        form =userauths_forms.LoginForm(request.POST or None)
        if form.is_valid():
            email= form.cleaned_data.get("email")
            password= form.cleaned_data.get("password")

            try:
                user_instance = userauths_forms.User.objects.get(email=email, is_active=True)
                user_authenticate = authenticate(request, email=email, password=password)
                
                if user_instance is not None:
                    login(request, user_authenticate)
                    
                    messages.success(request, "You are already logged in")
                    
                    next_url = request.GET.get("next", "/")
                    return redirect(next_url)
                else:
                    messages.error(request, "username or password does not exist!")
            except:
                messages.error(request, "username does not exist!")
        
    else:
        form = userauths_forms.LoginForm()

    context = {
            'form':form
    }
    return render(request, "userauths/sign-in.html", context) 
