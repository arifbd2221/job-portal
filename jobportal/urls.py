from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('managejob.urls')),
    path('', include('useraccount.urls')),
]
