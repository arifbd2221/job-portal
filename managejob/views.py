from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from .models import Job, Applicant
from useraccount.models import User
from .forms import *
from django.utils import timezone
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


JOB_TYPE = [
    "Full time",
    "Part time",
    "Internship",
    "Freelance",
    "Termporary",
]


class HomeView(ListView):
    model = Job
    template_name = 'managejob/index.html'
    context_object_name = 'jobs'
    paginate_by = 5
    ordering = ['-created_at']

    def get_queryset(self):
        return self.model.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        context['JOB_TYPE'] = JOB_TYPE
        return context

def newPost(request):
    return render(request, 'managejob/new-post.html', {})

def about(request):
    return render(request, 'managejob/about.html', {})

def contact(request):
    return render(request, 'managejob/contact.html', {})

def blog(request):
    return render(request, 'managejob/blog.html', {})


class SearchView(ListView):
    model = Job
    template_name = 'managejob/search.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_queryset(self):
        cat = self.request.GET.get('cat')
        jobtype = self.request.GET.get('type')
        loc = self.request.GET.get('loc')
        return self.model.objects.filter(category=cat, jobtype=jobtype, location=loc)



class JobCreateView(CreateView):
    template_name = 'managejob/new-post.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url =  reverse_lazy('home')

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('login')
        print("current page")
        return super().dispatch(self.request, *args, **kwargs)
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DashboardView(ListView):
    model = Job
    template_name = 'managejob/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'jobid'
    slug_url_kwarg = 'jobid'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'employee':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('home'))

    def get_success_url(self):
        return reverse_lazy('home')#, kwargs={'id': self.kwargs['job_id']})


    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user=self.request.user, job=self.kwargs['jobid'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

def applyjob(request, jobid):
    applicant = Applicant.objects.filter(user=request.user, job=jobid)
    job = Job.objects.get(id=jobid)
    if applicant:
        messages.info(request, 'You already applied for this job')
        return HttpResponseRedirect(reverse_lazy('home'))
    else:
        Applicant.objects.create(user=request.user, job=job)
        return HttpResponseRedirect(reverse_lazy('home'))
    

class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'managejob/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'managejob/all-applicants.html'
    context_object_name = 'applicants'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('login')
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(user=self.request.user)



class JobDetailsView(DetailView):
    model = Job
    template_name = 'managejob/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def delete(request, pk):
    try:
        query = Job.objects.get(id=pk)
        if query is not None:
            query.delete()
    except Job.DoesNotExist:
        return reverse_lazy('home')
        
    return HttpResponse("Deleted Successfully")


class EditJob(UpdateView):
    model = Job
    template_name = 'managejob/new-post.html'
    success_url = reverse_lazy('dashboard')
    form_class = CreateJobForm
    pk_url_kwarg = 'id'
    context_object_name = 'job'


    def form_valid(self, form):
        job = form.save(commit=False)
        job.user = self.request.user
        job.created_at = timezone.now()
        job.save()

        return HttpResponse("Updated Successfully") 

