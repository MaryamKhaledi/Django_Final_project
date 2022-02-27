from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Email
from django.views.generic import ListView, DetailView


def home(request, pk):
    # render(request, 'mail_page/load.html', {'pk':pk})
    return HttpResponse(f"{pk}'re welcome")
