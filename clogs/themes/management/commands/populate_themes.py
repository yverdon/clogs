from django.core.management.base import BaseCommand
from django.db import transaction

from clogs.themes import models


def create_interfaces():
    models.Interface.objects.all().delete()

    models.Interface.objects.create(
        name="Desktop",
        description="Interface desktop",
    )

    models.Interface.objects.create(
        name="Mobile",
        description="Interface mobile",
    )


def create_ogc_servers():

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


def create_themes():

    models.Theme.objects.all().delete()

    models.Theme.objects.create(
        name="Cadastre",
        icon="cadastre.svg",
        ordering=1,
        public=True,
    )

    models.Theme.objects.create(
        name="Environnement",
        icon="environnement.svg",
        ordering=2,
        public=True,
    )

    models.Theme.objects.create(
        name="Plan de Ville",
        icon="citymap.svg",
        ordering=3,
        public=True,
    )


def create_layers():

    models.Layer.objects.all().delete()
    models.LayerWms.objects.all().delete()
    models.LayerWmts.objects.all().delete()
    # Don't try this at home but use the admin interface, please
    layer_wms = models.Layer.objects.create(name="Layer WMS", public=True)
    layer_wms.interface.set(models.Interface.objects.all())

    models.LayerWms.objects.all().delete()

    models.LayerWms.objects.create(
        layer=layer_wms,
        ogc_server=models.OgcServer.objects.first(),
    )

    layer_wtms = models.Layer.objects.create(name="Layer WMTS Swisstopo", public=True)
    layer_wtms.interface.set(models.Interface.objects.all())

    models.LayerWmts.objects.all().delete()

    models.LayerWmts.objects.create(
        layer=layer_wtms,
    )


def create_layer_groups():

    models.LayerGroupMp.objects.all().delete()

    wms_layer = models.Layer.objects.get(name="Layer WMS")

    root_1 = models.LayerGroupMp.add_root(name="Points d'intérêts")
    root_1.layer.set([wms_layer])
    root_1.add_child(name="Mobilité")
    child_1 = root_1.add_child(name="Transports publics")
    child_1.add_child(name="Lignes de bus")
    child_1.add_child(name="Lignes de train")
    root_2 = models.LayerGroupMp.add_root(name="Mensuration")
    root_2.add_child(name="Limites")
    child_2 = root_2.add_child(name="Surfaces")
    child_2.add_child(name="Couveture du sol")


class Command(BaseCommand):
    help = "Populate basic themes, layer groups and layers"

    @transaction.atomic
    def handle(self, *args, **options):

        create_ogc_servers()
        create_interfaces()
        create_themes()
        create_layers()
        create_layer_groups()

        print(f"👥 added demo themes, layer groups and layers for demo!")
