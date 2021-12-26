from django.http import HttpResponse

from mortuary.models import Client, ClientBill


def generate_bills_for_monthly_clients(request):
    if request.headers.get('X-AppEngine-Cron'):
        monthly_clients = Client.objects.filter(assigned_products__isnull=False)
        generate_bills(monthly_clients)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


def generate_bills(monthly_clients):
    for client in monthly_clients:
        client_bill = ClientBill.objects.create(client=client, notes='Automatically monthly generated bill.')
        client_bill.generate_lines(client.assigned_products.all())
