# Create your views here.
from django.shortcuts import render
from django.core.management import call_command
from django.urls import reverse
from django.shortcuts import redirect



def home(request):
    return render(request, "home.html")


def clone_geoportal(request):

     if request.POST:
        geoportal_url = request.POST["geoportal_url"]
        call_command('clone_geoportal')

        return redirect(
            reverse(
                "admin:index",
            )
        )
