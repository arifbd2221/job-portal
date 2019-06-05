from django import forms
from .models import Job, Applicant


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

class CreateJobForm(forms.ModelForm):
    description = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'cols': 30, 'rows': 5}) )
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'col-lg-12 form-control'}), choices=CATEGORY_TYPE)
    jobtype = forms.ChoiceField(widget=forms.Select(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control'}), choices=JOB_TYPE)

    class Meta:
        model = Job
        exclude = ('user', 'created_at',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control'}),
            'validity': forms.TextInput(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control', 'type': 'date'}),
            'company': forms.TextInput(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control'}),
            'location': forms.TextInput(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control'}),
            'website': forms.TextInput(attrs={'class': 'col-md-12 mb-3 mb-md-0 form-control'}),
        }
    
    def is_valid(self):
        valid = super(CreateJobForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        job = super(CreateJobForm, self).save(commit=False)
        if commit:
            job.save()
        return job

class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ('job',)