from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('employee/register/', RegisterEmployeeView.as_view(), name='employee-register'),
    path('employer/register/', RegisterEmployerView.as_view(), name='employer-register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('employee/profile/update', EditProfileView.as_view(), name='employer-profile-update'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)