from django.urls import path
from .views import *

app_name = 'billmanagement'

urlpatterns = [

    # bill
    path('billlist/', billList, name='billlist'),
    path('billform/', billFormPage, name='billform'),
    path('billinvoice/<pk>/', BillInvoice, name='billinvoice'),
    path('billapprove/', billApprove, name='billapprove'),
    path('billstatus/<pk>/', BillStatus, name='billstatus'),

    # conveyance
    path('conveyancelist/', conveyanceList, name='conveyancelist'),
    path('conveyanceform/', conveyanceFormPage, name='conveyanceform'),
    path('conveyanceapprove/', conveyanceApprove, name='conveyanceapprove'),

]