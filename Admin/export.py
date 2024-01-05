
from django.template.loader import get_template
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa 
from Developer.models import *
from .filters import *
from django.contrib import messages
import csv
from django.contrib.staticfiles.storage import staticfiles_storage
from django.db.models import Min, Max

def export_invoice_list_pdf(request): 
    template = get_template('admin__export_invoice_list.html')  
    rec = Invoice.objects.select_related().order_by('id')
    Filter=Invoice_List_Filter(request.GET, queryset=rec)
    invoice_rec=Filter.qs  
    
    start_date = invoice_rec.aggregate(Min('invoice_date'))['invoice_date__min']
    end_date = invoice_rec.aggregate(Max('invoice_date'))['invoice_date__max'] 
    context = {
        "invoice_rec":invoice_rec,
        'start_date':start_date,
        'end_date':end_date
    }  
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice Records.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)


def export_invoice_list_csv(request): 
    rec = Invoice.objects.select_related().order_by('id')
    Filter = Invoice_List_Filter(request.GET, queryset=rec)
    invoice_rec = Filter.qs 

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Invoice_Records.csv"'

    # Create a CSV writer
    csv_writer = csv.writer(response)
    
    # Write the header row
    header_row = ['Invoice Date', 'Invoice Number', 'Dealer', 'Grand Total']
    csv_writer.writerow(header_row)

    # Write the data rows
    for invoice in invoice_rec:
        data_row = [
            invoice.invoice_date.strftime('%d-%m-%y'),  # Format the date as needed
            invoice.invoice_number,
            invoice.dealer,
            invoice.grand_total,
        ]
        csv_writer.writerow(data_row)

    return response



def export_transaction_list_pdf(request): 
    template = get_template('admin__export_transaction_list.html')  

    rec = Account.objects.select_related().order_by('id')
    Filter=Transaction_List_Filter(request.GET, queryset=rec)
    transaction_rec=Filter.qs 
    start_date = transaction_rec.aggregate(Min('transaction_date'))['transaction_date__min']
    end_date = transaction_rec.aggregate(Max('transaction_date'))['transaction_date__max']

    count=transaction_rec.count()
    # start_date = request.GET.get('start_date', None)
    # end_date = request.GET.get('end_date', None)
    context = {
        "transaction_rec":transaction_rec,
        'start_date':start_date,
        'end_date':end_date
    }  
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Transaction Records.pdf"'
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF file: %s' % pdf.err, status=400)



def export_transaction_list_csv(request):
    # Fetch the account records based on your filter logic if needed
    rec = Account.objects.select_related().order_by('id')
    Filter = Transaction_List_Filter(request.GET, queryset=rec)
    account_records = Filter.qs 

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Transaction_Records.csv"'

    # Create a CSV writer
    csv_writer = csv.writer(response)
    
    # Write the header row
    header_row = ['Dealer', 'Payment Mode', 'Transaction Date', 'Credit','Debit', 'Amount', 'Balance','Invoice Number', 'Remark']
    csv_writer.writerow(header_row)

    # Write the data rows
    for account in account_records:
        data_row = [
            account.dealer.business_name,  # Assuming Dealer has a 'name' field, replace with the actual field
            account.payment_mode,
            account.transaction_date.strftime('%d-%m-%y %H:%M:%S'),  # Format the date as needed
            "Credit" if account.is_credit else "",
            "Debit" if not account.is_credit else "",
            account.amount,
            account.balance,
            account.invoice_number, 
            account.remark,
        ]
        csv_writer.writerow(data_row)

    return response



def export_stock_details_csv(request):
    rec = Product.objects.select_related()  
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Stock Details.csv"'
    csv_writer = csv.writer(response)
    header_row = ['Product Code', 'Product Name', 'Minimum Stock Range', 'Available Stock']
    csv_writer.writerow(header_row)
    for product in rec:
        data_row = [
            product.product_code,  
            product.product_name,  
            product.minimum_stock,  
            product.available_stock,   
        ]
        csv_writer.writerow(data_row)
    return response