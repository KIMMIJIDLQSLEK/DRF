from django.urls import path
from . import views

urlpatterns = [
    path('quest/', views.quest),
]