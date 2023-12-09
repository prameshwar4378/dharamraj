from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum

class CustomUser(AbstractUser):
    name = models.CharField( max_length=50)
    designation = models.CharField( max_length=50)
    is_admin=models.BooleanField(default=False)
    profile_image=models.ImageField(upload_to="prifile_images", max_length=500)
    def __str__(self):
        return self.username


GST_FOR_PRODUCT=(
    ("6","6"),
    ("12","12"),
    ("18","18"),
)



class State(models.Model):
    state_name=models.CharField(max_length=20)
    def __str__(self):
        return self.state_name

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=40, db_index=True)
    business_name = models.CharField(max_length=40, db_index=True)
    mobile_no = models.CharField(max_length=12, db_index=True)
    email_id = models.CharField(max_length=40, db_index=True)
    address = models.CharField(max_length=200)
    state = models.ForeignKey(State, on_delete=models.CASCADE, db_index=True)
    pin_code = models.CharField(max_length=30,null=True, db_index=True)
    gst_number=models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.business_name

class Product(models.Model):
    product_code = models.CharField(max_length=20, unique=True, db_index=True)
    product_name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(null=True, blank=True)
    sale_amount=models.IntegerField(null=True)
    hsn_sac=models.IntegerField(null=True)
    gst=models.CharField(max_length=50,choices=GST_FOR_PRODUCT,null=True)
    available_stock = models.PositiveIntegerField(default=0, db_index=True)

    def __str__(self):
        return self.product_name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.available_stock += self.quantity
        self.product.save()

    def __str__(self):
        return f"{self.quantity} {self.product} purchased on {self.purchase_date}"


from django.utils import timezone

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, db_index=True)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, db_index=True)
    invoice_date = models.DateField(db_index=True, auto_now_add=True, auto_now=False)
    total_gst_amount = models.IntegerField(null=True, blank=True)
    grand_total = models.IntegerField(null=True, blank=True)
    is_added_in_account=models.BooleanField(default=False)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} for {self.dealer}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Auto-generate invoice_number
            prefix = 'DHRMJ'
            year = timezone.now().year
            next_invoice_number = Invoice.objects.filter(
                invoice_number__startswith=f'{prefix}{year}'
            ).count() + 1
            self.invoice_number = f'{prefix}{year}{next_invoice_number:06d}'
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            # Iterate over related InvoiceItems and update associated product's available_stock
            for invoice_item in self.invoiceitem_set.all():
                product = invoice_item.product
                product.available_stock += invoice_item.quantity
                product.save()
            
            super().delete(*args, **kwargs)

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField()
    rate = models.IntegerField()
    gst_percent = models.FloatField()
    taxable_amount = models.IntegerField()
    gst_amount = models.IntegerField()
    total_amount = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.available_stock -= self.quantity
        self.product.save() 

        # Update GST amount in associated Invoice
        invoice_items = InvoiceItem.objects.filter(invoice=self.invoice)
        total_gst_amount = invoice_items.aggregate(total_gst_amount=Sum('gst_amount'))['total_gst_amount']
        self.invoice.total_gst_amount = total_gst_amount
        self.invoice.save()
        
        # Update grand total in associated Invoice
        grand_total = invoice_items.aggregate(total_total_amount=Sum('total_amount'))['total_total_amount']
        self.invoice.grand_total = grand_total
        self.invoice.save()
    
    def __str__(self):
        return f"{self.quantity} {self.product}"
    
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            product = self.product
            invoice = self.invoice
            product.available_stock += self.quantity
            invoice.grand_total -= self.total_amount
            invoice.total_gst_amount -= self.gst_amount
            product.save()
            invoice.save()
            super().delete(*args, **kwargs)

            invoice_items = InvoiceItem.objects.filter(invoice=self.invoice)
            grand_total = invoice_items.aggregate(total_total_amount=models.Sum('total_amount'))['total_total_amount']
            self.invoice.grand_total = grand_total
            self.invoice.save()

PAYMENT_MODE = (
    ('Phone Pay', 'Phone Pay'),
    ('Credit Card', 'Credit Card'),
    ('Bank Transfer', 'Bank Transfer'),
    ('Cash', 'Cash'),
    ('Check', 'Check'),  # Added 'Check' as a new choice
)

class Account(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, db_index=True)
    amount = models.PositiveIntegerField()
    payment_mode = models.CharField(max_length=50, choices=PAYMENT_MODE)
    transaction_date = models.DateTimeField(auto_now_add=True, db_index=True)
    is_credit=models.BooleanField(default=True)
    balance = models.IntegerField(default=0, null=True)
    remark = models.TextField(blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_transactions')
    modified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_transactions')
    


    # def save(self, *args, **kwargs):
    #    # Retrieve the count and latest balance record for the dealer
    #     acc_rec_count = Account.objects.filter(dealer=self.dealer).count()
    #     if acc_rec_count:
    #         balance_rec = Account.objects.filter(dealer=self.dealer).latest('id')
    #     # Update the balance based on whether it's a credit or debit
    #     if self.is_credit:
    #         self.balance = balance_rec.balance + self.amount if acc_rec_count > 0 else self.amount
    #     else:
    #         self.balance = balance_rec.balance - self.amount if acc_rec_count > 0 else self.amount
    #     # If a record is being deleted, invert the process
    #     if kwargs.get('force_delete', False):
    #         if self.is_credit:
    #             self.balance = balance_rec.balance - self.amount if acc_rec_count > 0 else -self.amount
    #         else:
    #             self.balance = balance_rec.balance + self.amount if acc_rec_count > 0 else -self.amount
    #     # Call the parent class's save method to save the changes
    #     super(Account, self).save(*args, **kwargs)
 
    def __str__(self):
        return f"Transaction #{self.amount} {self.payment_mode}"
