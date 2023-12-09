
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .export import *
urlpatterns = [
  path('',index, name='admin_home'), 
  path('dashboard/',dashboard, name='admin_dashboard'), 

  path('user_list/',user_list, name='admin_user_list'), 
  path('update_user/<int:id>',update_user, name='admin_update_user'), 
  path('delete_user/<int:id>',delete_user, name='admin_delete_user'), 

  path('dealer_list/',dealer_list, name='admin_dealer_list'), 
  path('create_dealer/',create_dealer, name='admin_create_dealer'), 
  path('update_dealer/',update_dealer, name='admin_update_dealer'), 
  path('delete_dealer/<int:id>',delete_dealer, name='admin_delete_dealer'), 

  path('product_list/',product_list, name='admin_product_list'), 
  path('create_product/',create_product, name='admin_create_product'), 
  path('update_product/',update_product, name='admin_update_product'), 
  path('delete_product/<int:id>',delete_product, name='admin_delete_product'), 
  
  path('purchase_list/',purchase_list, name='admin_purchase_list'), 
  path('create_purchase/',create_purchase, name='admin_create_purchase'),
  # path('update_purchase/',update_purchase, name='admin_update_purchase'), 
  path('delete_purchase/<int:id>',delete_purchase, name='admin_delete_purchase'), 
  
  
  path('invoice_list/',invoice_list, name='admin_invoice_list'), 
  path('create_invoice/',create_invoice, name='admin_create_invoice'),
  path('update_invoice/',update_invoice, name='admin_update_invoice'), 
  path('delete_invoice/<int:id>',delete_invoice, name='admin_delete_invoice'), 
  path('add_invoice_in_account/<int:id>',add_invoice_in_account, name='admin_add_invoice_in_account'), 

  path('transaction_list/',transaction_list, name='admin_transaction_list'), 
  path('create_transaction/',create_transaction, name='admin_create_transaction'),
  path('update_transaction/',update_transaction, name='admin_update_transaction'), 
  path('delete_transaction/<int:id>',delete_transaction, name='admin_delete_transaction'), 

  path('invoice_item_list/<int:id>',invoice_item_list, name='admin_invoice_item_list'), 
  path('delete_invoice_item/<int:id>',delete_invoice_item, name='admin_delete_invoice_item'), 
  path('get_product_details/',get_product_details, name='admin_get_product_details'), 

  path('dealer_bulk_creation/',dealer_bulk_creation, name='admin_dealer_bulk_creation'), 
  path('product_bulk_creation/',product_bulk_creation, name='admin_product_bulk_creation'), 

  path('print_all_bills_formate/<int:id>',print_all_bills_formate, name='admin_print_all_bills_formate'), 
  path('troubleshoot_transactions_for_balance/',troubleshoot_transactions_for_balance, name='admin_troubleshoot_transactions_for_balance'), 


  path('export_invoice_list_pdf/',export_invoice_list_pdf, name='admin_export_invoice_list_pdf'), 
  path('export_invoice_list_csv/',export_invoice_list_csv, name='admin_export_invoice_list_csv'), 
  path('export_transaction_list_csv/',export_transaction_list_csv, name='admin_export_transaction_list_csv'), 
  path('export_transaction_list_pdf/',export_transaction_list_pdf, name='admin_export_transaction_list_pdf'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
