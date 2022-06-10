from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def quest(request):
    return JsonResponse({'message':'success'})