from django.shortcuts import render

def handler(request):
    return render(request, 'in_lucru.html')