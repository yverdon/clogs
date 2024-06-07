import orjson
from django.forms.models import model_to_dict
from django.http import HttpResponse

from .models import OgcServer, Theme


# Create the json for interface configuration
# WARNING: this should not be used in production as way too many DB queries are generated
# Goal is just to rapidly be able to check the geogiface comppliance of the endpoint
def themes(self):

    gg = {}
    ogc_servers = list(OgcServer.objects.all().values())
    gg["ogcServer"] = ogc_servers
    gg["background_layers"] = []

    themes_config = []
    for theme in Theme.objects.all():

        theme_dict = model_to_dict(theme)

        themes_nodes = []
        nodes = theme.layergroupmp.all().prefetch_related("layer")
        for node in nodes:
            node_dict = node.dump_bulk()
            themes_nodes.append(node_dict)

        del theme_dict["layergroupmp"]
        theme_dict["children"] = themes_nodes
        themes_config.append(theme_dict)

    gg["themes"] = themes_config

    return HttpResponse(orjson.dumps(gg), content_type="application/json")
