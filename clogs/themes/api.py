import orjson
from django.forms.models import model_to_dict
from django.http import HttpResponse

from .models import Layer, OgcServer, Theme


# Create the json for interface configuration
# WARNING: this should not be used in production as way too many DB queries are generated
# Goal is just to rapidly be able to check the geogiface comppliance of the endpoint
def themes(self):

    # layergoups = LayerGroupMp.objects.all().prefetch_related("layer")
    # for group in layergoups:
    #     print(group.layer.all())

    gg = {}
    ogc_servers = list(OgcServer.objects.all().values())
    gg["ogcServer"] = ogc_servers
    gg["background_layers"] = []

    layers_qs = (
        Layer.objects.all().prefetch_related("metadata").prefetch_related("interface")
    )

    themes_config = []
    themes_qs = (
        Theme.objects.all()
        .prefetch_related("layergroupmp")
        .prefetch_related("layergroupmp__layer")
    )
    for theme in themes_qs:

        theme_dict = model_to_dict(theme)

        themes_nodes = []
        # Get nodes associated with the current theme
        nodes = theme.layergroupmp.all()
        for node in nodes:
            node_dict = node.dump_bulk()
            themes_nodes.append(node_dict)

        del theme_dict["layergroupmp"]
        theme_dict["children"] = themes_nodes
        themes_config.append(theme_dict)

    # set related values for layers

    gg["themes"] = themes_config

    return HttpResponse(orjson.dumps(gg), content_type="application/json")
