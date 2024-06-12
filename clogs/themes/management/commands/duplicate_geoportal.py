from django.core.management.base import BaseCommand
from django.db import transaction

from clogs.themes import models
import json

import requests

def load_geoportal(url):

    models.Theme.objects.all().delete()
    r = requests.get(url)
    data = json.loads(r.content)
    for theme in data["themes"]:
        new_theme = models.Theme.objects.create(
            name=theme["name"],
            icon=theme["icon"],
            ordering=1,
            public=True,
        )

        #TODO: recursive parsing
        for child in theme["children"]:
            #TODO: don't duplicate
            group = models.LayerGroupMp.add_root(name=child["name"])
            new_theme.layergroupmp.add(group)





class Command(BaseCommand):
    help = "Populate basic themes, layer groups and layers"

    @transaction.atomic
    def handle(self, *args, **options):
        load_geoportal("https://mapnv.ch/themes")

        print(f"👥 added demo themes, layer groups and layers from existing geoportal!")
