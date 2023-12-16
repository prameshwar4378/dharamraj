import django_filters
from django import forms
from Developer.models import *
from django_filters import DateFilter
from django.forms import DateInput
 
class Invoice_List_Filter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='invoice_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='invoice_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    ) 
    grand_total__gte = django_filters.NumberFilter(
        field_name='grand_total',
        lookup_expr='gte',
        label='Grand Total Greater Than or Equal To'
    )
    grand_total__lte = django_filters.NumberFilter(
        field_name='grand_total',
        lookup_expr='lte',
        label='Grand Total Less Than or Equal To'
    )
    def __init__(self, *args, **kwargs):
        super(Invoice_List_Filter, self).__init__(*args, **kwargs)
        self.filters['invoice_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['invoice_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = Invoice
        fields = ['invoice_date','invoice_number','dealer','grand_total']
        widgets = {
            'invoice_date': DateInput(attrs={'type': 'date'})
        }



class Transaction_List_Filter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='transaction_date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    ) 
    balance__gte = django_filters.NumberFilter(
        field_name='balance',
        lookup_expr='gte',
        label='Balance Greater Than or Equal To'
    )
    balance__lte = django_filters.NumberFilter(
        field_name='balance',
        lookup_expr='lte',
        label='Balance Less Than or Equal To'
    )
    def __init__(self, *args, **kwargs):
        super(Transaction_List_Filter, self).__init__(*args, **kwargs)
        self.filters['transaction_date'].label = "Start Date - MM/DD/YYYY"
        self.filters['transaction_date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = Account
        fields = ['dealer','transaction_date','is_credit','balance']
        widgets = {
            'invoice_date': DateInput(attrs={'type': 'date'})
        }


 
class Performa_Invoice_List_Filter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        widget=DateInput(attrs={'type': 'date'}),
        label='End Date'
    ) 
     
    def __init__(self, *args, **kwargs):
        super(Performa_Invoice_List_Filter, self).__init__(*args, **kwargs)
        self.filters['date'].label = "Start Date - MM/DD/YYYY"
        self.filters['date'].label = "End Date - MM/DD/YYYY"

    class Meta:
        model = PerformaInvoice
        fields = ['performa_invoice_number','gst_number','date','mobile','state']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }
