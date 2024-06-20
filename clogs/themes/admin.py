from adminsortable2.admin import SortableAdminMixin
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from clogs.themes import models

app = apps.get_app_config("themes")



class LayerWmsInline(admin.StackedInline):
    model = models.LayerWms
    extra = 0
    can_delete = False
    verbose_name = _("Configuration WMS")
    verbose_name_plural = _("Configurations WMS")


class LayerWmsAdmin(admin.ModelAdmin):
    model = models.LayerForLayerWmsAdmin
    list_display = ("name",)
    inlines = (LayerWmsInline,)
    def get_queryset (self, request):
        return models.LayerForVectorTileAdmin.objects.filter(layerwms__isnull=False)


class LayerWmtsInline(admin.StackedInline):
    model = models.LayerWmts
    extra = 0
    can_delete = False
    verbose_name = _("Configuration WTMS")
    verbose_name_plural = _("Configurations WTMS")


class LayerWmtsAdmin(admin.ModelAdmin):
    model = models.LayerForLayerWmtsAdmin
    list_display = ("name",)
    inlines = (LayerWmtsInline,)
    def get_queryset (self, request):
        return models.LayerForVectorTileAdmin.objects.filter(layerwmts__isnull=False)



class LayerVectorTileInline(admin.StackedInline):
    model = models.LayerVectortiles
    extra = 0
    can_delete = False
    inline_classes = ("collapse open",)
    min_num = 1
    verbose_name = _("Configuration Vector Tile")
    verbose_name_plural = _("Configurations Vector Tiles")


class LayerVectorTilesAdmin(admin.ModelAdmin):
    model = models.LayerForVectorTileAdmin
    inlines = (LayerVectorTileInline,)
    def get_queryset (self, request):
        return models.LayerForVectorTileAdmin.objects.filter(layervectortile__isnull=False)



class LayerGroupMpAdmin(TreeAdmin):
    form = movenodeform_factory(models.LayerGroupMp)
    list_display = ("name",)


class RoleInline(admin.StackedInline):
    model = models.Role
    can_delete = False
    verbose_name_plural = "Role"
    inline_classes = ("collapse open",)
    min_num = 1


class UserInline(admin.TabularInline):
    model = Group.user_set.through
    readonly_fields = ("user",)
    can_delete = False
    extra = 0
    verbose_name = _("Utilisateur membre du groupe")
    verbose_name_plural = _("Utilisateurs membres du groupe")


class GroupAdmin(BaseGroupAdmin):
    model = Group
    inlines = (RoleInline, UserInline)


class FunctionalityInlines(admin.TabularInline):
    model = models.Theme.functionality.through
    extra = 2
    verbose_name = _("Fonctionnalité")
    verbose_name_plural = _("Fonctionnalités")

class MetadataInlines(admin.TabularInline):
    model = models.Theme.metadata.through
    extra = 2
    verbose_name = _("Métadonnée")
    verbose_name_plural = _("Métadonnées")

class LayergroupmpInlines(admin.TabularInline):
    model = models.Theme.layergroupmp.through
    extra = 2
    verbose_name = _("Groupe de couche")
    verbose_name_plural = _("Groupes de couches")

class interfaceInlines(admin.TabularInline):
    model = models.Theme.interface.through
    extra = 2
    verbose_name = _("Interface")
    verbose_name_plural = _("Interfaces")


class GroupForThemeInline(admin.TabularInline):
    model = models.Theme.group.through
    can_delete = False
    extra = 2
    verbose_name = _("Role")
    verbose_name_plural = _("Roles")



class ThemeAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = [
        "functionality",
        "metadata",
        "layergroupmp",
        "group",
        "interface",
    ]
    model = models.Theme
    inlines = [LayergroupmpInlines, GroupForThemeInline, FunctionalityInlines, MetadataInlines, interfaceInlines]

    fieldsets = [
        (
            None,
            {
                "fields": ["name", "icon", "public",],
            },
        ),
    ]


class GroupInline(admin.TabularInline):
    model = models.Restrictionarea.group.through
    can_delete = False
    extra = 2
    verbose_name = _("Groupe")
    verbose_name_plural = _("Groupes")


class RestrictionareaAdmin(admin.ModelAdmin):
    exclude = ["layer", "group"]
    model = models.Restrictionarea
    inlines = [GroupInline]


admin.site.register(models.LayerGroupMp, LayerGroupMpAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(models.Theme, ThemeAdmin)
admin.site.register(models.LayerForLayerWmsAdmin, LayerWmsAdmin)
admin.site.register(models.LayerForLayerWmtsAdmin, LayerWmtsAdmin)
admin.site.register(models.LayerForVectorTileAdmin, LayerVectorTilesAdmin)
admin.site.register(models.OgcServer)
admin.site.register(models.Restrictionarea, RestrictionareaAdmin)
admin.site.register(models.Functionality)
admin.site.register(models.Interface)
admin.site.register(models.Metadata)
