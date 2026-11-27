from django.shortcuts import render
from django.contrib import messages

def handler(request):
  messages.error(request, "This is a test error message.")
  messages.warning(request, "This is a test warning message.")
  messages.success(request, "This is a test success message.")
  messages.info(request, "This is a test info message.")
  messages.debug(request, "This is a test debug message.")
  
  return render(request, 'test.html')