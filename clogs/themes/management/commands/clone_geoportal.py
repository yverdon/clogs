import json

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from clogs.themes import models


def import_layergroups(children, new_theme=None, parent_node=None):
    print("Recursing theme's layer groups...")
    # List of theme's related layer groups, or layer groups related layer groups...
    for child in children:
        # First level
        if new_theme:
            # TODO: don't create duplicates
            group = models.LayerGroupMp.add_root(name=child["name"])
            new_theme.layergroupmp.add(group)
        # Other levels
        if parent_node:
            # TODO: don't create duplicates
            group = parent_node.add_child(name=child["name"])

            if "layers" in child:
                layer = models.Layer.objects.create(
                    name=child["name"],
                )
                layer.layergroupmp.add(group)
                if child["type"] == "WMS":
                    models.LayerWms.objects.create(
                        layer=layer,
                        ogc_server=models.OgcServer.objects.first(),
                    )

        if len(child.keys()) > 1:
            for key, value in child.items():
                if key == "children":
                    import_layergroups(value, parent_node=group)


def load_geoportal(url):

    models.Theme.objects.all().delete()
    models.LayerGroupMp.objects.all().delete()
    models.Layer.objects.all().delete()
    models.LayerWms.objects.all().delete()
    r = requests.get(url)
    data = json.loads(r.content)
    for theme in data["themes"]:
        new_theme = models.Theme.objects.create(
            name=theme["name"],
            icon=theme["icon"],
            ordering=1,
            public=True,
        )

        import_layergroups(theme["children"], new_theme)


class Command(BaseCommand):
    help = "Populate basic themes, layer groups and layers"

    @transaction.atomic
    def handle(self, *args, **options):

        # TODO: load ogc serve from json, this is a dummy one!
        models.OgcServer.objects.all().delete()

        models.OgcServer.objects.create(
            name="OGC QGIS Server",
            description="QGIS server",
            url="https://ogc.mapnv.ch/wms-mapnv",
            type="QGIS server",
            image_type="image/png",
            wfs_support=True,
            is_single_tile=True,
        )
        load_geoportal("https://map.geo.bs.ch/themes")

        print(f"👥 added demo themes, layer groups and layers from existing geoportal!")
