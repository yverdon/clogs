from ninja import NinjaAPI, Schema

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


class ThemeSchema(Schema):
    id: int
    name: str
    icon: str
    layergroupmp: list["LayerGroupSchema"] = []
    functionality: list[FunctionalitySchema] = []
    metadata: list[MetadataSchema] = []


@api.get("/themes")
def themes(request):
    return LayergroupSchema.from_treebeard_dump(models.LayerGroupMp.dump_bulk())


@api.get("/geogirafe")
def geogirafe(request):
    return {
        "themes": themes(request),
        "ogcServers": "not implemented",
        "background_layers": "not implemented",
    }
