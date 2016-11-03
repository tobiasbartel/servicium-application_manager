from django.contrib import admin
from servicecatalog.models import *
from reversion_compare.admin import CompareVersionAdmin
from guardian.admin import GuardedModelAdmin
from pprint import pprint
from guardian.shortcuts import assign_perm, get_group_perms
from django.contrib import messages

class module_writeing_to_module(admin.TabularInline):
    model = ModuleWritesToModule
    fk_name = 'from_module'
    extra = 1

class contacts_for_module(admin.TabularInline):
    model = ModuleContact
    fk_name = 'parent'
    extra = 1

class PaymentMethodAdmin(GuardedModelAdmin, CompareVersionAdmin):

    def get_queryset(self, request):
        qs = super(PaymentMethodAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            for object in qs:
                keep = False
                for group in request.user.groups.all():
                    if u'is_owner' in get_group_perms(group, object):
                        keep = True
                if not keep:
                    qs = qs.exclude(pk=object.pk)
                pprint(keep)
            return qs

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            my_group = request.user.groups.all().get(name__contains='TEAM_')
            assign_perm('is_owner', my_group, obj)
admin.site.register(PaymentMethod, PaymentMethodAdmin)

class ModuleAdmin(GuardedModelAdmin, CompareVersionAdmin):
    inlines = (contacts_for_module, module_writeing_to_module, )
    prepopulated_fields = { "slug": ("name",) }

    def get_queryset(self, request):
        qs = super(ModuleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            for object in qs:
                keep = False
                for group in request.user.groups.all():
                    if u'is_owner' in get_group_perms(group, object):
                        keep = True
                if not keep:
                    qs = qs.exclude(pk=object.pk)
                pprint(keep)
            return qs

    def save_model(self, request, obj, form, change):
        obj.save()
        if not change:
            my_group = request.user.groups.all().get(name__contains='TEAM_')
            assign_perm('is_owner', my_group, obj)
admin.site.register(Module, ModuleAdmin)