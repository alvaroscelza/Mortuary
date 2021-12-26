from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _

from utils.mixins import NameMixin, TimeStampMixin


class Provider(TimeStampMixin, NameMixin):
    company_name = models.CharField(verbose_name=_('company name'), max_length=50, blank=True)
    address = models.CharField(verbose_name=_('address'), max_length=100, blank=True)
    phone = models.CharField(verbose_name=_('phone'), max_length=50, blank=True)
    bank_account_information = models.CharField(verbose_name=_('bank account information'), max_length=100, blank=True)
    notes = models.CharField(verbose_name=_('notes'), max_length=200, blank=True)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('provider')
        verbose_name_plural = _('providers')


class Product(TimeStampMixin, NameMixin):
    internal_reference = models.CharField(verbose_name=_('internal reference'), max_length=50, blank=True)
    sell_price = models.FloatField(verbose_name=_('sell price'), default=0)
    buy_price = models.FloatField(verbose_name=_('buy price'), default=0)
    client_taxes_percentage = models.IntegerField(verbose_name=_('client taxes percentage'), default=22,
                                                  validators=[MinValueValidator(0), MaxValueValidator(100)])
    internal_notes = models.CharField(verbose_name=_('internal notes'), max_length=200, blank=True)
    # image = models.ImageField(verbose_name=_('image'), upload_to='product', default='product/default_image.png')
    provider = models.ForeignKey(Provider, verbose_name=_('provider'), on_delete=models.PROTECT)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('product')


class Client(TimeStampMixin):
    name = models.CharField(verbose_name=_('name'), max_length=50)
    lastname = models.CharField(verbose_name=_('lastname'), max_length=50)
    document = models.IntegerField(verbose_name=_('document'))
    phone = models.CharField(verbose_name=_('phone'), max_length=50, blank=True)
    birthdate = models.DateField(verbose_name=_('birthdate'))
    address = models.CharField(verbose_name=_('address'), max_length=50)
    payment_address = models.CharField(verbose_name=_('payment address'), max_length=50)
    assigned_products = models.ManyToManyField(Product, verbose_name=_('assigned products'), blank=True)
    assigned_vendor = models.ForeignKey(User, verbose_name=_('assigned vendor'), on_delete=models.PROTECT)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('client')

    def __str__(self):
        return '{} {}'.format(self.name, self.lastname)


class Bill(TimeStampMixin):
    date = models.DateField(verbose_name=_('date'), default=datetime.now)
    total_to_pay = models.FloatField(verbose_name=_('total to pay'),
                                     default=0)  # TODO: calculate from all bill's lines subtotals. Should not be editable
    notes = models.CharField(verbose_name=_('notes'), max_length=100, blank=True)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('bill')


class BillLine(TimeStampMixin):
    product = models.ForeignKey(Product, verbose_name=_('product'), on_delete=models.PROTECT)
    notes = models.CharField(verbose_name=_('notes'), max_length=100, blank=True)
    amount = models.IntegerField(verbose_name=_('amount'), validators=[MinValueValidator(1)])
    price = models.FloatField(
        verbose_name=_('price'))  # TODO: calculate from product sell or buy price depending on bill type
    taxes_percentage = models.IntegerField(verbose_name=_('taxes percentage'),
                                           validators=[MinValueValidator(0), MaxValueValidator(
                                               100)])  # TODO: calculate from client taxes if it's a client's bill
    subtotal = models.FloatField(verbose_name=_('subtotal'),
                                 default=0)  # TODO: calculate from amount, price and taxes. Should not be editable
    bill = models.ForeignKey(Bill, verbose_name=_('bill'), on_delete=models.CASCADE)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('bill line')


class ClientBill(Bill):
    client = models.ForeignKey(Client, verbose_name=_('client'), on_delete=models.PROTECT)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('client bill')

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.client, self.total_to_pay)

    def generate_lines(self, products):
        for product in products:
            bill_line = BillLine.objects.create(product=product, amount=1, price=product.sell_price,
                                                taxes_percentage=product.client_taxes_percentage,
                                                subtotal=1 * product.sell_price * float(
                                                    product.client_taxes_percentage / 100 + 1),
                                                bill=self)
            self.total_to_pay += bill_line.subtotal
            self.save()


class ProviderBill(Bill):
    provider = models.ForeignKey(Provider, verbose_name=_('provider'), on_delete=models.PROTECT)

    class Meta:
        app_label = __name__.split(".")[0]
        verbose_name = _('provider bill')
        verbose_name_plural = _('provider bills')

    def __str__(self):
        return '{} - {} - {}'.format(self.date, self.provider, self.total_to_pay)
