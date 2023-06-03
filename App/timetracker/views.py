from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

# Import time
from datetime import datetime, timedelta
from .models import Project, TimeEntry
from .forms import AddProjectForm


@login_required
def projects(request):
    formWasSuccess = 0
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = AddProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # Check if Project for that user with the same name already exists
            if Project.objects.filter(name=form.cleaned_data['name'], owner=request.user).exists():
                formWasSuccess = -1 # Project already exists
            else:
                Project.objects.create(name=form.cleaned_data['name'], slug=form.cleaned_data['name'].replace(" ", "-"), owner=request.user, default_rate=form.cleaned_data['rate']),
                formWasSuccess = 1 # Project created successfully

    form = AddProjectForm()

    try:
        myprojects = Project.objects.filter(owner=request.user).values()
    except:
        myprojects = None
    template = loader.get_template('all_projects.html')

    def total_time_last_week_all_projects_hours():
        total_time = 0
        for project in myprojects:
            result = TimeEntry.objects.filter(project=project['id'], start_time__gte=datetime.now()-timedelta(days=7)).aggregate(duration=Sum('duration'))['duration']
            if result is not None:
                total_time += result
        total_time = total_time / 3600
        return total_time

    def projects_added_last_week():
        projects_added = 0
        if myprojects != None:
            for project in myprojects:
                try:
                    #Get first time entry from project
                    firstTimeEntry = TimeEntry.objects.filter(project=project['id']).order_by('start_time').first()
                    firstTimeEntry = int(round(firstTimeEntry.start_time.timestamp()))
                    sevenDaysAgo = int(round((datetime.now() - timedelta(days=7)).timestamp()))
                    if firstTimeEntry > sevenDaysAgo:
                        projects_added += 1
                except:
                    pass
        return projects_added

    def total_time_all_projects_hours():
        if myprojects is not None:
            result = Project.objects.filter(owner=request.user).aggregate(total_time=Sum('total_time'))['total_time']
            if result is not None:
                return result/3600
        return 0

    def revenue_project(project):
        total_revenue = 0
        for time_entry in TimeEntry.objects.filter(project=project['id']):
            total_revenue += time_entry.rate * (time_entry.duration/3600)
        return total_revenue

    def revenue_all_projects():
        total_revenue = 0
        for project in myprojects:
            total_revenue += revenue_project(project)
        return total_revenue

    def revenue_project_last_week(project):
        total_revenue = 0
        for time_entry in TimeEntry.objects.filter(project=project['id'], start_time__gte=datetime.now()-timedelta(days=7)):
            total_revenue += time_entry.rate * (time_entry.duration/3600)
        return total_revenue

    def revenue_all_projects_last_week():
        total_revenue = 0
        if myprojects is not None:
            for project in myprojects:
                total_revenue += revenue_project_last_week(project)
        return total_revenue

    context = {
        'myprojects': myprojects,
        'runningprojects': Project.objects.filter(owner=request.user, is_recording=True).values(),
        'projects_added_last_week' : projects_added_last_week(),
        'time_projects_all' : total_time_all_projects_hours(),
        'time_projects_week' : total_time_last_week_all_projects_hours(),
        'revenue_projects_all' : revenue_all_projects(),
        'revenue_projects_week' : revenue_all_projects_last_week(),
        'form': form,
        'formWasSuccess': formWasSuccess,
        'avatar' : request.user.profile.avatar.url,
    }
    return HttpResponse(template.render(context, request))

@login_required
def details(request, slug):
    myproject = Project.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'myproject': myproject,
        'runningprojects': Project.objects.filter(owner=request.user, is_recording=True).values(),
        'time_entries': TimeEntry.objects.filter(project_id=myproject.id).values(),
        'avatar' : request.user.profile.avatar.url,
    }
    return HttpResponse(template.render(context, request))

@login_required
def delete(request, id):
    Project.objects.filter(id=id, owner=request.user).delete()
    return HttpResponseRedirect('/projects/')

@login_required
def start_timer(request, id):
    # Check if Project is already running -> do nothing
    if not Project.objects.filter(id=id, owner=request.user, is_recording=True).exists():
        # Create new TimeEntry for this Project
        TimeEntry.objects.create(project_id=id, start_time=datetime.now(), rate=Project.objects.get(id=id).default_rate)
        # Set Project.is_recording to True
        Project.objects.filter(id=id, owner=request.user).update(is_recording=True)
    return HttpResponseRedirect('/projects/')

@login_required
def stop_timer(request, id):
    # Check if project is running -> if not do nothing
    if Project.objects.filter(id=id, owner=request.user, is_recording=True).exists():
        # Get TimeEntry for this Project
        mytimeentry = TimeEntry.objects.get(project_id=id, end_time=None)
        # Update TimeEntry.end_time
        mytimeentry.end_time = datetime.now()
        mytimeentry.duration = int(mytimeentry.end_time.timestamp() - mytimeentry.start_time.timestamp()) # In Seconds
        
        mytimeentry.save()

        # Update Project is_recording and total_time
        project_time = Project.objects.get(id=id, owner=request.user).total_time
        Project.objects.filter(id=id, owner=request.user).update(is_recording=False, total_time = mytimeentry.duration + project_time)
    
    return HttpResponseRedirect('/projects/')

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
