from django.db import models
from django.utils import timezone
from useraccount.models import User

JOB_TYPE = (
    ('Full-time', "Full time"),
    ('Part-time', "Part time"),
    ('Internship', "Internship"),
    ('Freelance', "Freelance"),
    ('Termporary', "Termporary"),
)


CATEGORY_TYPE = (
    ('Web-design', "Web design"),
    ('Graphic-design', "Graphic design"),
    ('Web-development', "Web development"),
    ('Human-Resources', "Human Resources"),
    ('Support', "Support"),
    ('Android', "Android"),
)

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_TYPE, max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    jobtype = models.CharField(choices=JOB_TYPE, max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    website = models.CharField(max_length=100, default="")
    validity = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()