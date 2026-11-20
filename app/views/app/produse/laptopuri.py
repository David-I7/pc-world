from django.shortcuts import render
from ....models import Laptop

def handler(request):
    laptopuri = Laptop.objects.all()
    return render(request, 'in_lucru.html')