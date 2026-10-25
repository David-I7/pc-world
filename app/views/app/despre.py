from django.shortcuts import render

def handler(request):
    return render(request, 'app/despre.html')