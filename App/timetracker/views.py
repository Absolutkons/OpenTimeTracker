from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Project

def timetracker(request):
    template = loader.get_template('timetracker.html')
    return HttpResponse(template.render())

#@login_required
def projects(request):
    myprojects = Project.objects.all().values()
    template = loader.get_template('all_projects.html')
    context = {
        'myprojects': myprojects,
    }
    return HttpResponse(template.render(context, request))

#@login_required
def details(request, slug):
    myproject = Project.objects.get(slug=slug)
    template = loader.get_template('details.html')
    context = {
        'myproject': myproject,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())
