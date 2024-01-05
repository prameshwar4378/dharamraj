
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from .export import *
urlpatterns = [ 
  path('dashboard/',dashboard, name='staff_dashboard'), 
 
  path('dealer_list/',dealer_list, name='staff_dealer_list'), 
  path('create_dealer/',create_dealer, name='staff_create_dealer'), 
  path('update_dealer/',update_dealer, name='staff_update_dealer'), 
  path('delete_dealer/<int:id>',delete_dealer, name='staff_delete_dealer'), 

  path('product_list/',product_list, name='staff_product_list'), 
  path('create_product/',create_product, name='staff_create_product'), 
  path('update_product/',update_product, name='staff_update_product'), 
  path('delete_product/<int:id>',delete_product, name='staff_delete_product'), 
  
  path('purchase_list/',purchase_list, name='staff_purchase_list'), 
  path('create_purchase/',create_purchase, name='staff_create_purchase'),
  # path('update_purchase/',update_purchase, name='staff_update_purchase'), 
  path('delete_purchase/<int:id>',delete_purchase, name='staff_delete_purchase'), 
  
  
  path('invoice_list/',invoice_list, name='staff_invoice_list'), 
  path('create_invoice/',create_invoice, name='staff_create_invoice'),
  path('update_invoice/',update_invoice, name='staff_update_invoice'), 
  path('delete_invoice/<int:id>',delete_invoice, name='staff_delete_invoice'), 
  path('add_invoice_in_account/<int:id>',add_invoice_in_account, name='staff_add_invoice_in_account'), 

  path('transaction_list/',transaction_list, name='staff_transaction_list'), 
  path('create_transaction/',create_transaction, name='staff_create_transaction'),
  path('update_transaction/',update_transaction, name='staff_update_transaction'), 
  path('delete_transaction/<int:id>',delete_transaction, name='staff_delete_transaction'), 
  path('print_transactions_receipt/<int:id>',print_transactions_receipt, name='staff_print_transactions_receipt'), 

  path('invoice_item_list/<int:id>',invoice_item_list, name='staff_invoice_item_list'), 
  path('delete_invoice_item/<int:id>',delete_invoice_item, name='staff_delete_invoice_item'), 
  path('get_product_details/',get_product_details, name='staff_get_product_details'), 

  path('dealer_bulk_creation/',dealer_bulk_creation, name='staff_dealer_bulk_creation'), 
  path('product_bulk_creation/',product_bulk_creation, name='staff_product_bulk_creation'), 

  path('print_all_invoice_formate/<int:id>',print_all_invoice_formate, name='staff_print_all_invoice_formate'), 
  path('troubleshoot_transactions_for_balance/',troubleshoot_transactions_for_balance, name='staff_troubleshoot_transactions_for_balance'), 


  path('export_invoice_list_pdf/',export_invoice_list_pdf, name='staff_export_invoice_list_pdf'), 
  path('export_invoice_list_csv/',export_invoice_list_csv, name='staff_export_invoice_list_csv'), 
  path('export_transaction_list_csv/',export_transaction_list_csv, name='staff_export_transaction_list_csv'), 
  path('export_transaction_list_pdf/',export_transaction_list_pdf, name='staff_export_transaction_list_pdf'), 
  path('export_stock_details_csv/',export_stock_details_csv, name='staff_export_stock_details_csv'), 

  # performa Invoice Links
  path('performa_invoice_list/',performa_invoice_list, name='staff_performa_invoice_list'), 
  path('create_performa_invoice/',create_performa_invoice, name='staff_create_performa_invoice'),  
  path('update_performa_invoice/',update_performa_invoice, name='staff_update_performa_invoice'), 
  path('delete_performa_invoice/<int:id>',delete_performa_invoice, name='staff_delete_performa_invoice'), 
  
  path('performa_invoice_item_list/<int:id>',performa_invoice_item_list, name='staff_performa_invoice_item_list'), 
  path('delete_performa_invoice_item/<int:id>',delete_performa_invoice_item, name='staff_delete_performa_invoice_item'), 
  path('print_performa_invoice/<int:id>',print_performa_invoice, name='staff_print_performa_invoice'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
