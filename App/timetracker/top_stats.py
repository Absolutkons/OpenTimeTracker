from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Project, TimeEntry

def total_time_last_week_all_projects_hours(myprojects):
    total_time = 0
    for project in myprojects:
        result = TimeEntry.objects.filter(project=project['id'], start_time__gte=datetime.now()-timedelta(days=7)).aggregate(duration=Sum('duration'))['duration']
        if result is not None:
            total_time += result
    total_time = total_time / 3600
    return total_time

def projects_added_last_week(myprojects):
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

def total_time_all_projects_hours(request, myprojects):
    if myprojects is not None:
        result = Project.objects.filter(owner=request.user).aggregate(total_time=Sum('total_time'))['total_time']
        if result is not None:
            return result/3600
    return 0

def revenue_project(myprojects):
    total_revenue = 0
    for time_entry in TimeEntry.objects.filter(project=myprojects['id']):
        total_revenue += time_entry.rate * (time_entry.duration/3600)
    return total_revenue

def revenue_all_projects(myprojects):
    total_revenue = 0
    for project in myprojects:
        total_revenue += revenue_project(project)
    return total_revenue

def revenue_project_last_week(myprojects):
    total_revenue = 0
    for time_entry in TimeEntry.objects.filter(project=myprojects['id'], start_time__gte=datetime.now()-timedelta(days=7)):
        total_revenue += time_entry.rate * (time_entry.duration/3600)
    return total_revenue

def revenue_all_projects_last_week(myprojects):
    total_revenue = 0
    if myprojects is not None:
        for project in myprojects:
            total_revenue += revenue_project_last_week(project)
    return total_revenue

def workload_current_week(myprojects):
    workload = 0
    for project in myprojects:
        workload += TimeEntry.objects.filter(project=project['id'], start_time__gte=datetime.now()-timedelta(days=7)).aggregate(duration=Sum('duration'))['duration']
    return workload

def workload_current_month(myprojects):
    workload = 0
    for project in myprojects:
        workload += TimeEntry.objects.filter(project=project['id'], start_time__gte=datetime.now()-timedelta(days=30)).aggregate(duration=Sum('duration'))['duration']
    return workload