from django.contrib.auth.models import Group
from django.contrib.gis.db import models as gismodels
from django.core import serializers
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from treebeard.mp_tree import MP_Node


class Interface(models.Model):

    """
    Model that matches a configuration with a interface configuration (desktop, mobile, api, ...)
    """

    name = models.CharField()
    description = models.CharField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Interface")
        verbose_name_plural = _("Interfaces")

    def __str__(self):
        return f"{self.name}"


class Theme(models.Model):
    """
    Top item of layer tree organization
    """

    name = models.CharField(max_length=64)
    icon = models.CharField(blank=True, null=True)
    ordering = models.IntegerField()
    public = models.BooleanField()
    functionality = models.ManyToManyField("Functionality", blank=True)
    interface = models.ManyToManyField(
        "Interface", related_name="theme_interface", blank=True
    )
    metadata = models.ManyToManyField(
        "Metadata", related_name="theme_metadata", blank=True
    )
    layergroupmp = models.ManyToManyField(
        "LayerGroupMp", related_name="theme_layergroupmp", blank=True
    )
    group = models.ManyToManyField(Group, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ["ordering"]
        verbose_name = _("Thème")
        verbose_name_plural = _("Thèmes")

    def __str__(self):
        return f"{self.name}"


class LayerGroupMp(MP_Node):
    """
    Recursive model from django-treebeard to handle children-parent relationships
    """

    name = models.CharField(max_length=30)
    layer = models.ManyToManyField("Layer", related_name="layergroupmp", blank=True)
    node_order_by = ["name"]

    class Meta:
        verbose_name = _("Groupede de couche")
        verbose_name_plural = _("Groupes de couche")

    def __str__(self):
        return f"Groupe: {self.name}"

    @classmethod
    def dump_bulk(cls, parent=None, keep_ids=True):
        """Dumps a tree branch to a python data structure.
        From: https://github.com/django-treebeard/django-treebeard/blob/fe35cd2d33bed11946f8c28ee34aa2aaca2de73d/treebeard/mp_tree.py#L626
        """

        # TODO: is that useful in clogs case ?
        # cls = get_result_class(cls)

        # Because of fix_tree, this method assumes that the depth
        # and numchild properties in the nodes can be incorrect,
        # so no helper methods are used
        qset = (
            cls._get_serializable_model()
            .objects.all()
            .prefetch_related("layer")
            .prefetch_related("layer__metadata")
            .prefetch_related("layer__interface")
        )
        if parent:
            qset = qset.filter(path__startswith=parent.path)
        ret, lnk = [], {}
        pk_field = cls._meta.pk.attname
        for pyobj in serializers.serialize("python", qset):
            # django's serializer stores the attributes in 'fields'
            fields = pyobj["fields"]
            path = fields["path"]
            depth = int(len(path) / cls.steplen)
            # this will be useless in load_bulk
            del fields["depth"]
            del fields["path"]
            del fields["numchild"]
            if pk_field in fields:
                # this happens immediately after a load_bulk
                del fields[pk_field]

            newobj = {"data": fields}
            if keep_ids:
                newobj[pk_field] = pyobj["pk"]

            if (not parent and depth == 1) or (
                parent and len(path) == len(parent.path)
            ):
                ret.append(newobj)
            else:
                parentpath = cls._get_basepath(path, depth - 1)
                parentobj = lnk[parentpath]
                if "children" not in parentobj:
                    parentobj["children"] = []
                parentobj["children"].append(newobj)
            lnk[path] = newobj

        return ret


class Layer(models.Model):
    """
    Base model for geographic Layer
    """

    name = models.CharField(blank=True, null=True)
    public = models.BooleanField(blank=True, null=True)
    geo_table = models.CharField(blank=True, null=True)
    exclude_properties = models.CharField(blank=True, null=True)
    interface = models.ManyToManyField(
        "Interface",
        blank=True,
    )
    metadata = models.ManyToManyField(
        "Metadata", related_name="layer_metadata", blank=True
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Couche")
        verbose_name_plural = _("Couches")

    def __str__(self):
        return f"{self.name}"


class Dimension(models.Model):
    name = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    layer = models.ForeignKey("Layer", models.DO_NOTHING)
    field = models.CharField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Dimension")
        verbose_name_plural = _("Dimensions")

    def __str__(self):
        return f"{self.name}"


class Functionality(models.Model):
    name = models.CharField()
    value = models.CharField()
    description = models.CharField(blank=True, null=True)
    group = models.ManyToManyField(Group)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Fonctionnalité")
        verbose_name_plural = _("Fonctionnalités")

    def __str__(self):
        return f"{self.name}"


class LayerVectortiles(models.Model):
    """
    Layer extension for vector tile layer
    """

    layer = models.OneToOneField(
        Layer,
        on_delete=models.CASCADE,
        related_name="layervectortile",
        null=True,
    )
    style = models.CharField()
    xyz = models.CharField(blank=True, null=True)
    sql = models.CharField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Vector Tile")
        verbose_name_plural = _("Vector Tiles")

    def __str__(self):
        return f"{self.layer.name}"


class LayerWms(models.Model):
    """
    Layer extension for WMS layer"""

    layer = models.OneToOneField(
        Layer,
        on_delete=models.CASCADE,
        related_name="layerwms",
        null=True,
    )
    ogc_server = models.ForeignKey("OgcServer", models.DO_NOTHING)
    style = models.CharField(blank=True, null=True)
    time_mode = models.CharField(blank=True, null=True)
    time_widget = models.CharField(blank=True, null=True)
    valid = models.BooleanField(blank=True, null=True)
    invalid_reason = models.CharField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Couche WMS")
        verbose_name_plural = _("Couches WMS")

    def __str__(self):
        return f"{self.layer.name}"


class LayerWmts(models.Model):
    """
    Layer extension for WMTS layer"""

    layer = models.OneToOneField(
        Layer,
        on_delete=models.CASCADE,
        related_name="layerwmts",
        null=True,
    )
    url = models.URLField()
    style = models.CharField(blank=True, null=True)
    matrix_set = models.CharField(blank=True, null=True)
    image_type = models.CharField(max_length=10)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Couche WMTS")
        verbose_name_plural = _("Couches WMTS")

    def __str__(self):
        return f"{self.layer.name}"


class Metadata(models.Model):
    """
    Generic Model for fine grained configuration
    """

    name = models.CharField(blank=True, null=True)
    value = models.CharField(blank=True, null=True)
    description = models.CharField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Métadonnée")
        verbose_name_plural = _("Métadonnées")

    def __str__(self):
        return f"{self.name}"


class OgcServer(models.Model):
    """
    Definition of cartographic servers that can be selected when configurating layers
    """

    name = models.CharField(unique=True)
    description = models.CharField(blank=True, null=True)
    url = models.URLField()
    url_wfs = models.URLField(blank=True, null=True)
    type = models.CharField()
    image_type = models.CharField()
    auth = models.CharField()
    wfs_support = models.BooleanField(blank=True, null=True)
    is_single_tile = models.BooleanField(blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Serveur OGC")
        verbose_name_plural = _("Serveurs OGC")

    def __str__(self):
        return f"{self.name}"


# Move to users app ?
class Role(models.Model):
    """
    Extension of the Django Group model, adding geographic area
    for fine grained spatial access control
    """

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="role",
        null=True,
    )
    description = models.CharField(blank=True, null=True)
    extent = gismodels.MultiPolygonField(null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


# Move to users app ?
class Restrictionarea(models.Model):
    """
    Model that defines a geographic area that group (role) can see or edit
    """

    name = models.CharField()
    description = models.CharField(blank=True, null=True)
    readwrite = models.BooleanField(blank=True, null=True)
    area = gismodels.PolygonField(null=True)
    buffer = models.TextField(blank=True, null=True)
    layer = models.ManyToManyField(Layer)
    group = models.ManyToManyField(Group)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Aire de restriction")
        verbose_name_plural = _("Aires de restriction")

    def __str__(self):
        return f"{self.layer.name}"
