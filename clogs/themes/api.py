from typing import List

from ninja import ModelSchema, NinjaAPI, Schema

from . import models

api = NinjaAPI()


class FunctionalitySchema(Schema):
    id: int
    name: str
    value: str


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


# WIP, need to retrieve all layer related models
class LayerSchema(Schema):
    id: int | list[int] | None = None
    name: str | list[str] | None = None
    metadata: MetadataSchema | list[MetadataSchema] | None = None
    interface: MetadataSchema | list[MetadataSchema] | None = None


class OgcserverSchema(Schema):
    id: int
    name: str


class LayergroupSchema(Schema):
    id: int
    name: str
    layer: list[LayerSchema]
    children: list["LayergroupSchema"]

    @classmethod
    def from_treebeard_dump(cls, data: dict) -> list["LayergroupSchema"]:
        return [
            cls(
                id=item["id"],
                name=item["data"]["name"],
                layer=item["data"]["layer"],
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


@api.get("/geogirafe")
def geogirafe(request):
    return {
        "themes": layergroups(request),
        "ogcServers": "not implemented",
        "background_layers": "not implemented",
    }
