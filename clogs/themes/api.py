from ninja import ModelSchema, NinjaAPI, Schema, Field
from ninja.orm.fields import AnyObject

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


class OgcserverSchema(Schema):
    id: int
    name: str
    wms: str = Field(None, alias="url")
    wfsUrl: str = Field(None, alias="url_wfs")
    type: str
    credential: bool = True #FIXME
    imageType: str = Field(None, alias="image_type")
    wfsSupport: bool = Field(None, alias="wfs_support")
    isSingleType: bool = Field(None, alias="is_single_tile")
    namespace: str = ""
    attributes: AnyObject



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


class ThemeSchema(ModelSchema):
    metadata: list[MetadataSchema]
    functionality: list[FunctionalitySchema]
    interface: list[InterfaceSchema]

    class Meta:
        model = models.Theme
        fields = "__all__"

@api.get("/themes")
def themes(request):

    ogcservers = models.OgcServer.objects.all()
    ogcservers_dict = {}
    for server in ogcservers:
        ogcservers_dict[server.name] = OgcserverSchema.from_orm(server).dict()
    layergroups_data = [
        LayergroupSchema.from_orm(i).dict()
        for i in LayergroupSchema.from_treebeard_dump(models.LayerGroupMp.dump_bulk())
    ]

    # move layers into children's list to be geogirafe compliant
    # we can't use alias here as the "children" key is already used in Schema
    # FIXME: fix performance leak
    layergroups_data_refactored = []
    for layergroup in layergroups_data:
        if layergroup["layers"]:
            for layer in layergroup["layers"]:
                layergroup["children"].append(layer)
        layergroups_data_refactored.append(layergroup)

    themes = models.Theme.objects.all()
    themes_data = [ThemeSchema.from_orm(i).dict() for i in themes]
    output_themes_data = []
    # Add related groups to themes
    # FIXME: fix performance leak
    for theme in themes_data:
        theme["children"] = []
        for related_group in theme["layergroupmp"]:
            for group in layergroups_data_refactored:
                if group["id"] == related_group:
                    theme["children"].append(group)
        output_themes_data.append(theme)

    return {
        "ogcServers": ogcservers_dict,
        "themes": output_themes_data,
        # TODO: implements optional objects
        "background_layers": [], 
        "errors": [],
    }
