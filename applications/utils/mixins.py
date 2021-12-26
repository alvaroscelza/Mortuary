import csv

from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True)

    class Meta:
        abstract = True


class NameMixin(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ExporterAdminMixin(admin.ModelAdmin):
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    actions = [export_as_csv]
    export_as_csv.short_description = "Export Selected as CSV"

    class Meta:
        abstract = True
