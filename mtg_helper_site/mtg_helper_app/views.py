from django.http import HttpResponse
import configparser

import mysql.connector

from .models import Neo

from django.shortcuts import render 
from rest_framework import generics
from .serializers import NeoSerializer
from .models import Neo 

class NeoView(generics.CreateAPIView):
  class Meta: 
    queryset = Neo.objects.all()
    seriazer_class = NeoSerializer

def index(request):
    neo = Neo.objects.all()
    context = {
      'neo' : neo
    }    
    return render(request, 'index.html', context)