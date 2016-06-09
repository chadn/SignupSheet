import textwrap

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms 
from django.http import Http404

from models import Coordinator, Job, Role, Source, Volunteer
from django.shortcuts import render, redirect

class SignupForm(forms.Form):
    name = forms.CharField(label='Name')
    comment = forms.CharField(label='Comment', required=False)
    def clean(self):
        super(SignupForm, self).clean()

def default(request):
    source = Source.objects.order_by('title')
    if len(source) == 0 :
        response_text = textwrap.dedent('''
          <html>
          <head>
          <title>Be the Ball</title>
          </head>
          <body>
          <p>A flute with no hole is not a flute.</p>
          <p>A doughnut without a hole is a danish.</p>
          </body>
        </html>''')
        return HttpResponse(response_text)    
    return redirect('jobs', source[0].title)

def jobs(request, title):
    # Fetch the role information 
    source = Source.objects.filter(title__exact=title)
    role = Role.objects.filter(source__exact=source[0])[0]
    coordinators = Coordinator.objects.filter(source__exact=source[0])
    jobs = Job.objects.filter(source__exact=source[0])
    
    # Now find the people that are signed up
    jobstaff = []
    for job in jobs :
        entry = {}
        entry['job'] = job
        entry['volunteers'] = []
        for volunteer in Volunteer.objects.filter(source__exact=job.source.pk, title__exact=job.title, start__exact=job.start) :
            vol = {}
            vol['volunteer'] = volunteer
            if request.user == volunteer.user :
                vol['can_delete'] = volunteer.id
            else:
                vol['can_delete'] = None
                
            entry['volunteers'].append(vol)
        entry['can_signup'] = len(entry['volunteers']) < job.needs
        
        jobstaff.append(entry)
        
    template_values = {
        'source': source[0],
        'role': role,
        'coordinators' : coordinators,
        'jobs' : jobstaff,
        'next' : title,
    }
    return render_to_response('signup/jobpage.html', context=template_values)

def signup(request, pk, template_name='signup/signup.html'):
    job = Job.objects.get(pk=pk)
    if job == None :
        raise Http404("Job does not exist")

    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid() :            
            # Create a Volunteer with form data 
            # We need the natural key from the job... this way 
            # if the job changes in a non-meaningful way this volunteer
            # continues to be valid. 
            v = Volunteer(
                user = request.user,
                name = form.cleaned_data['name'],
                comment = form.cleaned_data['comment'],
                source = job.source.pk,
                title = job.title, 
                start = job.start,
            )
            v.save()
            return redirect('jobs', job.source.pk)

        else:
            return render(request, template_name, {'form':form})
            
    else:
        ## Pre-fill the form with the user's name (They don't have to use it.)
        form = SignupForm({'name': request.user})
        return render(request, template_name, {'form':form, 'ret':job.source.pk})

def delete(request, pk, template_name='signup/confirmdelete.html'):
    volunteer = Volunteer.objects.get(pk=pk)
    if volunteer == None :
        raise Http404("Volunteer does not exist")

    if request.method=='POST':
        volunteer.delete()
        return redirect('jobs', volunteer.source)
    
    return render(request, template_name, {'object':volunteer, 'ret':volunteer.source})
