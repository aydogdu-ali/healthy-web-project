from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "base/index.html")


def service_detail(request, servise_id):
    return render(request, "base/service_detail.html")