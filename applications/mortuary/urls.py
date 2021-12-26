from django.urls import path

from mortuary import views

app_name = 'mortuary'

urlpatterns = [path('generate_bills_for_monthly_clients/', views.generate_bills_for_monthly_clients)]
