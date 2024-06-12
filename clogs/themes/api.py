from ninja import ModelSchema, NinjaAPI, Schema

from . import models

api = NinjaAPI()


class FunctionalitySchema(Schema):
    id: int
    name: str
    value: str


class OgcserverSchema(ModelSchema):
    class Meta:
        model = models.OgcServer
        fields = "__all__"


class MetadataSchema(ModelSchema):
    class Meta:
        model = models.Metadata
        fields = "__all__"


class FunctionalitySchema(ModelSchema):
    class Meta:
        model = models.Functionality
        fields = "__all__"


class InterfaceSchema(ModelSchema):
    class Meta:
        model = models.Interface
        fields = "__all__"


class OgcserverSchema(Schema):
    id: int
    name: str


class LayerSchema(ModelSchema):
    metadata: list[MetadataSchema]

    class Meta:
        model = models.Layer
        fields = [
            "id",
            "name",
            "public",
            "metadata",
        ]


class LayergroupSchema(Schema):
    id: int
    name: str
    layers: list[LayerSchema]
    children: list["LayergroupSchema"]

    @classmethod
    def from_treebeard_dump(cls, data: dict) -> list["LayergroupSchema"]:

        return [
            cls(
                id=item["id"],
                name=item["data"]["name"],
                layers=item["data"]["layer"],
                children=cls.from_treebeard_dump(item.get("children", [])),
            )
            for item in data
        ]


class LayergroupSchemaBasic(Schema):
    class Meta:
        model = models.LayerGroupMp
        fields = "__all__"


class ThemeSchema(ModelSchema):
    metadata: list[MetadataSchema]
    functionality: list[FunctionalitySchema]
    interface: list[InterfaceSchema]
    # TODO: add layergroups recursive m2m field

    class Meta:
        model = models.Theme
        fields = "__all__"


@api.get("/themes", response=list[ThemeSchema])
def themes(request):
    return (
        models.Theme.objects.all()
        .prefetch_related("metadata")
        .prefetch_related("interface")
        .prefetch_related("functionality")
    )


@api.get("/layergroups")
def layergroups(request):
    return LayergroupSchema.from_treebeard_dump(models.LayerGroupMp.dump_bulk())


@api.get("/ogcservers", response=list[OgcserverSchema])
def ogcservers(request):
    return models.OgcServer.objects.all()


@api.get("/geogirafe")
def geogirafe(request):
    return {
        "ogcServers": "not implemented",
        "themes": "not implemented",
        "background_layers": "not implemented",
        "errors": "not implemented",
    }
