# WIP !


from ninja import ModelSchema, NinjaAPI, Schema

from . import models

api = NinjaAPI()


class FunctionalitySchema(Schema):
    id: int
    name: str
    value: str


class MetadataSchema(Schema):
    id: int
    name: str
    value: str


class LayerSchema(ModelSchema):
    class Meta:
        model = models.Layer
        fields = ["id", "name"]


class OgcserverSchema(ModelSchema):
    class Meta:
        model = models.Layer
        fields = ["id", "name"]


class LayerGroupSchema(Schema):
    id: int
    name: str
    layergroupmp: "LayerGroupSchema" = None


class ThemeSchema(Schema):
    id: int
    name: str
    icon: str
    layergroupmp: list[LayerGroupSchema] = []
    functionality: list[FunctionalitySchema] = []
    metadata: list[MetadataSchema] = []


class GeogirafeSchema(Schema):
    ogcServer: list[OgcserverSchema] = []
    themes: list[ThemeSchema] = []
    backgroud_layers: str = None
    errors: str = None


class LayergroupOut(Schema):
    id: int
    name: str
    layer: LayerSchema = None
    children: list["LayergroupOut"]

    @classmethod
    def from_treebeard_dump(cls, data: dict) -> list["LayergroupOut"]:
        return [
            cls(
                id=item["id"],
                name=item["data"]["name"],
                children=cls.from_treebeard_dump(item.get("children", [])),
            )
            for item in data
        ]


@api.get("/themes")
def themes(request):
    return LayergroupOut.from_treebeard_dump(models.LayerGroupMp.dump_bulk())


@api.get("/geogirafe", response=list[GeogirafeSchema])
def themes(request):
    queryset = (
        models.Theme.objects.prefetch_related("functionality")
        .prefetch_related("metadata")
        .prefetch_related("layergroupmp")
        .prefetch_related("layergroupmp__layer")
    )
    return queryset
