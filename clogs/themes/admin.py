from adminsortable2.admin import SortableAdminMixin
from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from clogs.themes import models

app = apps.get_app_config("themes")


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


class LayergroupTreeitemInlines(admin.TabularInline):
    model = models.Theme.layergrouptreeitem.through
    extra = 2
    verbose_name = _("Groupe")
    verbose_name_plural = _("Groupes")


class FunctionalityInlines(admin.TabularInline):
    model = models.Theme.functionality.through
    extra = 2
    verbose_name = _("Fonctionnalité")
    verbose_name_plural = _("Fonctionnalités")


class ThemeAdmin(SortableAdminMixin, admin.ModelAdmin):
    exclude = [
        "layergrouptreeitem",
        "functionality",
    ]
    model = models.Theme
    inlines = [LayergroupTreeitemInlines, FunctionalityInlines]


class LayerInlines(admin.TabularInline):
    model = models.Restrictionarea.layer.through
    extra = 2
    verbose_name = _("Couche")
    verbose_name_plural = _("Couches")


class GroupInline(admin.TabularInline):
    model = models.Restrictionarea.group.through
    can_delete = False
    extra = 2
    verbose_name = _("Groupe")
    verbose_name_plural = _("Groupes")


class RestrictionareaAdmin(admin.ModelAdmin):
    exclude = ["layer", "group"]
    model = models.Restrictionarea
    inlines = [LayerInlines, GroupInline]


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(models.Theme, ThemeAdmin)
admin.site.register(models.Treeitem)
admin.site.register(models.LayergroupTreeitem)
admin.site.register(models.Treegroup)
admin.site.register(models.Layer)
admin.site.register(models.LayerWmts)
admin.site.register(models.LayerVectortiles)
admin.site.register(models.OgcServer)
admin.site.register(models.Restrictionarea, RestrictionareaAdmin)
admin.site.register(models.Functionality)
admin.site.register(models.Interface)
