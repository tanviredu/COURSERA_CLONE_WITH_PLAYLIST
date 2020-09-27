from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(ListView):
    model = Product
    template_name = "App_Shop/home.html"

class ProductDetail(LoginRequiredMixin,DetailView):
    model = Product
    template_name = "App_Shop/product_detail.html"

def all_courses(request):
    courses = Product.objects.all()
    return render(request,'App_Shop/all.html',{'courses':courses})
    