from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Rango says hey there partner!!!")


def about(request):
    return HttpResponse("Rango says this is about page!!!")
