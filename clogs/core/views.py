# Create your views here.
from django.shortcuts import render
from django.core.management import call_command
from django.urls import reverse
from django.shortcuts import redirect
from .forms import HomeForm, GEOPORTAL_URLS


def home(request):
 
    form = HomeForm()

    return render(request, "home.html", {"form": form})


def clone_geoportal(request):

    if request.method == "POST":
        form = HomeForm(request.POST)
        if form.is_valid():
            geoportal_url = GEOPORTAL_URLS[form.cleaned_data["geoportal_url"]]
            call_command('clone_geoportal', geoportal_url)

            return redirect(
                reverse(
                    "admin:index",
                )
            )
