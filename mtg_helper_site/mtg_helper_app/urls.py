from django.urls import path

from .views import NeoView

urlpatterns = [
    path('', NeoView.as_view(), name='neo'),
]