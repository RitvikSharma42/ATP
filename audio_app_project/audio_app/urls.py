# audio_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_audio, name='record_audio'),
    path('faq/', views.faq_view, name='faq'),
    path('product-list/', views.product_list_view, name='product_list'),
    path('display_output/', views.display_output, name='display_output'),
]
