from django.shortcuts import render
from django.http import HttpRequest
import os

# from ../icpcsite import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAINSITE_DIR = os.path.dirname(BASE_DIR)
BACK_BASE = os.path.dirname(MAINSITE_DIR)
SITE_BASE = os.path.dirname(BACK_BASE)
FRONT_BASE = os.path.join(SITE_BASE, "Front-End")
ACM_WEBSITE = os.path.join(FRONT_BASE, "acmWebsite")

# Create your views here.

def index(request):
    return render(request, 'index.html', {
        "PUBLIC_URL": os.path.join(ACM_WEBSITE, "public")
    })