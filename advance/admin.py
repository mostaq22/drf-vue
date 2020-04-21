from django.contrib import admin
from .models import Client, Category, Unit, Department, Project, Site, Requisition, RequisitionDetail

# Register your models here.

common_info_models = [Client, Category, Unit, Department]


class CommonInfoModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']


for model in common_info_models:
    admin.site.register(model, CommonInfoModelAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'client',
                    'department', 'requisition_manager', 'status']


class SiteAdmin(admin.ModelAdmin):
    # list_select_related = ('client', 'department')
    list_display = ['name', 'code', 'project', 'client',
                    'department', 'status']


class RequsitionDetailInline(admin.TabularInline):
    model = RequisitionDetail


class RequsitionAdmin(admin.ModelAdmin):
    inlines = [
        RequsitionDetailInline
    ]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(Requisition, RequsitionAdmin)
