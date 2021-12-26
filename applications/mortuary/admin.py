from django.contrib import admin
from django.utils.html import format_html

from mortuary.models import BillLine, Client, ClientBill, Product, Provider, ProviderBill
from utils.mixins import ExporterAdminMixin


@admin.register(Provider)
class ProviderAdminMixin(ExporterAdminMixin):
    list_display = ['name']


@admin.register(Product)
class ProductAdminMixin(ExporterAdminMixin):
    # def image_tag(self, product):
    #     return format_html('<img src="{}" width="100" height="100"/>'.format(product.image.url))
    #
    # image_tag.short_description = 'Image'
    # list_display = ['name', 'image_tag']
    list_display = ['name']


@admin.register(Client)
class ClientAdminMixin(ExporterAdminMixin):
    list_display = ['name', 'lastname', 'assigned_vendor']


class BIllLineInline(admin.TabularInline):
    model = BillLine
    template = "tabular.html"


class BillAdminMixin(ExporterAdminMixin):
    inlines = [BIllLineInline]


@admin.register(ClientBill)
class ClientBillAdmin(BillAdminMixin):
    list_display = ['id', 'date', 'client', 'total_to_pay']


@admin.register(ProviderBill)
class ProviderBillAdmin(BillAdminMixin):
    list_display = ['id', 'date', 'provider', 'total_to_pay']
