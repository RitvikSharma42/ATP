# audio_app_project/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from audio_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('audio_app.urls')),
    path('faq/', views.faq_view, name='faq'),
    path('output/', views.display_output, name='display_output'),
    path('products/', views.product_list_view, name='product_list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)