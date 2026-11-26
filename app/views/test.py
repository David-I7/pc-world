from django.http import JsonResponse

def handler(request, id, subpath):
  print(isinstance(id, int))  # True
  print(isinstance(subpath, str))  # True
  return JsonResponse({'id': id, 'subpath': subpath})