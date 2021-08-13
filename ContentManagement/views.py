from django.http import HttpResponse
from django.shortcuts import render
from ContentManagement import VisitStatistic
from django.utils.translation import gettext
import logging


# Create your views here.
def homepage(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'homepage.html', {"currentIP": currentIP, 'total_visit': totalVisit})


def ProjectDescription(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'ContentManagement/ProjectDescription.html',
                  {"currentIP": currentIP, 'total_visit': totalVisit})


def ProjectProgress(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'ContentManagement/ProjectProgress.html',
                  {"currentIP": currentIP, 'total_visit': totalVisit})


def ProjectMember(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'ContentManagement/ProjectMember.html', {"currentIP": currentIP, 'total_visit': totalVisit})


def ContactUs(request):
    currentIP, totalVisit = VisitStatistic.change_info(request)
    return render(request, 'ContentManagement/ContactUs.html', {"currentIP": currentIP, 'total_visit': totalVisit})


