from django.db import models
from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import Group

# TODOs:
# 1. Extend Group to have a polygon field

class Log(models.Model):
    date = models.DateTimeField()
    action = models.CharField()
    element_type = models.CharField(max_length=50)
    element_id = models.IntegerField()
    element_name = models.CharField()
    element_url_table = models.CharField()
    username = models.CharField()


class Shorturl(models.Model):
    url = models.CharField(blank=True, null=True)
    ref = models.CharField(unique=True, max_length=20)
    creator_email = models.CharField(max_length=200, blank=True, null=True)
    creation = models.DateTimeField(blank=True, null=True)
    last_hit = models.DateTimeField(blank=True, null=True)
    nb_hits = models.IntegerField(blank=True, null=True)


class Dimension(models.Model):
    name = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    layer = models.ForeignKey('Layer', models.DO_NOTHING)
    field = models.CharField(blank=True, null=True)


class Functionality(models.Model):
    name = models.CharField()
    value = models.CharField()
    description = models.CharField(blank=True, null=True)
    group = models.ManyToManyField(Group)


class Interface(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)


class Layer(models.Model):
    id = models.OneToOneField('Treeitem', models.DO_NOTHING, db_column='id', primary_key=True)
    public = models.BooleanField(blank=True, null=True)
    geo_table = models.CharField(blank=True, null=True)
    exclude_properties = models.CharField(blank=True, null=True)
    interface = models.ManyToManyField(Interface)


class LayerVectortiles(models.Model):
    id = models.OneToOneField(Layer, models.DO_NOTHING, db_column='id', primary_key=True)
    style = models.CharField()
    xyz = models.CharField(blank=True, null=True)
    sql = models.CharField(blank=True, null=True)


class LayerWms(models.Model):
    id = models.OneToOneField(Layer, models.DO_NOTHING, db_column='id', primary_key=True)
    ogc_server = models.ForeignKey('OgcServer', models.DO_NOTHING)
    layer = models.CharField()
    style = models.CharField(blank=True, null=True)
    time_mode = models.CharField()
    time_widget = models.CharField()
    valid = models.BooleanField(blank=True, null=True)
    invalid_reason = models.CharField(blank=True, null=True)


class LayerWmts(models.Model):
    id = models.OneToOneField(Layer, models.DO_NOTHING, db_column='id', primary_key=True)
    url = models.CharField()
    layer = models.CharField()
    style = models.CharField(blank=True, null=True)
    matrix_set = models.CharField(blank=True, null=True)
    image_type = models.CharField(max_length=10)


class Layergroup(models.Model):
    id = models.OneToOneField('Treegroup', models.DO_NOTHING, db_column='id', primary_key=True)


class LayergroupTreeitem(models.Model):
    treegroup = models.ForeignKey('Treegroup', models.DO_NOTHING)
    treeitem = models.ForeignKey('Treeitem', models.DO_NOTHING)
    ordering = models.IntegerField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)


class Log(models.Model):
    date = models.DateTimeField()
    action = models.CharField()
    element_type = models.CharField(max_length=50)
    element_id = models.IntegerField()
    element_name = models.CharField()
    element_url_table = models.CharField()
    username = models.CharField()


class Metadata(models.Model):
    name = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    item = models.ForeignKey('Treeitem', models.DO_NOTHING)


class OgcServer(models.Model):
    name = models.CharField(unique=True)
    description = models.CharField(blank=True, null=True)
    url = models.CharField()
    url_wfs = models.CharField(blank=True, null=True)
    type = models.CharField()
    image_type = models.CharField()
    auth = models.CharField()
    wfs_support = models.BooleanField(blank=True, null=True)
    is_single_tile = models.BooleanField(blank=True, null=True)


class Restrictionarea(models.Model):
    name = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    readwrite = models.BooleanField(blank=True, null=True)
    area = gismodels.PolygonField()
    buffer = models.TextField(blank=True, null=True)
    layer = models.ManyToManyField(Layer)
    group = models.ManyToManyField(Group)


class Role(models.Model):
    name = models.CharField(unique=True)
    description = models.CharField(blank=True, null=True)
    extent = models.TextField(blank=True, null=True)  # This field type is a guess.


class Theme(models.Model):
    id = models.OneToOneField('Treegroup', models.DO_NOTHING, db_column='id', primary_key=True)
    icon = models.CharField(blank=True, null=True)
    ordering = models.IntegerField()
    public = models.BooleanField()
    interface = models.ManyToManyField(Interface)
    group = models.ManyToManyField(Group)


class ThemeFunctionality(models.Model):
    theme = models.OneToOneField(Theme, models.DO_NOTHING, primary_key=True)  # The composite primary key (theme_id, functionality_id) found, that is not supported. The first column is selected.
    functionality = models.ForeignKey(Functionality, models.DO_NOTHING)

    class Meta:
        unique_together = (('theme', 'functionality'),)


class Treegroup(models.Model):
    id = models.OneToOneField('Treeitem', models.DO_NOTHING, db_column='id', primary_key=True)


class Treeitem(models.Model):
    type = models.CharField(max_length=10)
    name = models.CharField()
    description = models.CharField(blank=True, null=True)

    class Meta:
        unique_together = (('type', 'name'),)


class Tsearch(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(blank=True, null=True)
    layer_name = models.CharField(blank=True, null=True)
    ts = models.TextField(blank=True, null=True)  # This field type is a guess.
    the_geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    public = models.BooleanField(blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
    params = models.CharField(blank=True, null=True)
    interface = models.ForeignKey(Interface, models.DO_NOTHING, blank=True, null=True)
    lang = models.CharField(max_length=2, blank=True, null=True)
    actions = models.CharField(blank=True, null=True)
    from_theme = models.BooleanField(blank=True, null=True)