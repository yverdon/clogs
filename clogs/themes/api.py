from typing import List
from ninja import NinjaAPI, Schema, ModelSchema
from ninja.orm import create_schema
from . import models

api = NinjaAPI()


ThemeSchema = create_schema(
    models.Theme,
    depth=10,
    fields=['name', 'functionality', 'layergroupmp']
)


@api.get("/themes", response=List[ThemeSchema])
def themes(request):
    queryset = models.Theme.objects.all()
    return list(queryset)

