from os import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.Category.as_view(), name="Category"),
    path('product/', views.Product.as_view(), name="Product"),
]
