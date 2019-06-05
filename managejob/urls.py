from django.contrib import admin
from django.urls import path, include
from .views import HomeView, newPost, applyjob, delete, about,contact, blog, JobCreateView, DashboardView, SearchView, ApplyJobView, ApplicantsListView, ApplicantPerJobView, JobDetailsView, EditJob

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('newpost/', newPost, name='newpost'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('blog/', blog, name='blog'),
    path('employer/jobs/create/', JobCreateView.as_view(), name='employer-jobs-create'),
    path('employer/jobs/dashboard/', include([
        path('', DashboardView.as_view(), name='dashboard'),
        path('all-applicants/', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>/', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
    ])),
    path('jobs/search/', SearchView.as_view(), name='search'),
    path('applyjob/<int:jobid>/', applyjob, name='applyjob'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('delete/job/<int:pk>/', delete, name='delete-job'),
    path('update/job/<int:id>/', EditJob.as_view(), name='update-job'),
]