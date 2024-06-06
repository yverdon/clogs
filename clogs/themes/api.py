from typing import List

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
    layer: list[LayerSchema] = []


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


# https://github.com/fabiocaccamo/django-treenode/discussions/89


@api.get("/layers", response=list[LayerSchema])
def themes(request):
    queryset = models.Layer.objects.all()
    return queryset


@api.get("/themes", response=list[ThemeSchema])
def themes(request):
    queryset = (
        models.Theme.objects.prefetch_related("functionality")
        .prefetch_related("metadata")
        .prefetch_related("layergroupmp")
        .prefetch_related("layergroupmp__layer")
    )
    return queryset


@api.get("/geogirafe", response=list[GeogirafeSchema])
def themes(request):
    queryset = (
        models.Theme.objects.prefetch_related("functionality")
        .prefetch_related("metadata")
        .prefetch_related("layergroupmp")
        .prefetch_related("layergroupmp__layer")
    )
    return queryset
