from django.shortcuts import render
from django.http import HttpResponse


def say_hello(request):
    a = 5
    b = 10
    return render(request, 'hello.html', {'name': 'Raymond'})
