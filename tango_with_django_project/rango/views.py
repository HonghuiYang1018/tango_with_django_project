from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, cnady, cupckae'}
    
    return render(request, 'index.html', context = context_dict)


def about(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, cnady, cupckae', 'name':"BY Honghui Yang 2841006"}
    
    return render(request, 'about.html', context = context_dict)

