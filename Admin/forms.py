from django import forms
from Developer.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm 


class DealerCreationForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ('dealer_name','business_name','mobile_no','email_id','address','state','pin_code','gst_number')
        labels = { 
            'mobile_no': 'Mobile Number',
            'email_id': 'Email', 
            'dealer_name': 'Dealer Name', 
            'business_name': 'Business Name', 
            'pin_code': 'Pin Code', 
            'gst_number': 'GST Number', 
        }   
        
    # validatoions start     
    def clean_mobile_no(self):
        mobile = self.cleaned_data.get('mobile_no')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile
    

class DealerUpdateForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = ('dealer_name','business_name','mobile_no','email_id','address','state','pin_code','gst_number')
        labels = { 
            'mobile_no': 'Mobile Number',
            'email_id': 'Email', 
            'dealer_name': 'Dealer Name', 
            'business_name': 'Business Name', 
            'pin_code': 'Pin Code', 
            'gst_number': 'GST Number', 
        }   
        
    # validatoions start     
    def clean_mobile_no(self):
        mobile = self.cleaned_data.get('mobile_no')
        if mobile:
            if not mobile.isdigit() or len(mobile) != 10:
                raise ValidationError('Enter a valid 10 digit mobile number.')
        return mobile
    

        

class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_code','product_name','description','sale_amount','gst','hsn_sac','minimum_stock')
        labels = { 
            'sale_amount': 'NDP Amount',
            'product_code': 'Product Code', 
            'gst': 'GST %', 
            'hsn_sac': 'HSN/SAC Code', 
            'minimum_stock':'Minimum Stock for Alert',
        }  
        
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_code','product_name','description','sale_amount','gst','hsn_sac','minimum_stock')
        labels = { 
            'sale_amount': 'NDP Amount',
            'product_code': 'Product Code', 
            'gst': 'GST %', 
            'hsn_sac': 'HSN/SAC Code', 
            'minimum_stock':'Minimum Stock for Alert',
        }  

class PurchaseCreationForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('product','quantity')
      
class PurchaseUpdateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('product','quantity')
             
    


class InvoiceCreationForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ( 'dealer',) 
      
class InvoiceUpdateForm(forms.ModelForm):
    class Meta: 
        model = Invoice
        fields = ( 'dealer',) 
       
      
class InvoiceProductForm(forms.ModelForm):
    class Meta: 
        model = InvoiceItem
        fields = ('product','quantity','rate','gst_percent','taxable_amount','gst_amount','total_amount')
        widgets = {
            'product': forms.Select(attrs={'onchange': 'get_details()'}), 
            'quantity': forms.TextInput(attrs={'oninput': 'generate_amount()'}), 
            'rate': forms.TextInput(attrs={'oninput': 'generate_amount()'}), 
            'gst_percent': forms.TextInput(attrs={'oninput': 'generate_amount()','readonly': True}), 
            'gst_amount': forms.TextInput(attrs={'readonly': True}), 
            'taxable_amount': forms.TextInput(attrs={'readonly': True}), 
            'total_amount': forms.TextInput(attrs={'readonly': True}), 
            # 'rate': forms.TextInput(attrs={'readonly': True}), 
        }
        labels = { 
            'rate': 'Basic Amount',
            'taxable_amount': 'Taxable Amount', 
            'gst_percent': 'GST %', 
            'gst_amount': 'GST Amount', 
            'total_amount': 'Total Amount', 
        } 



class User_Creation(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    class Meta:
        model = CustomUser
        fields = ('username','name','designation','profile_image','password1','password2')
 
class User_Updation(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'Confirm Password'})
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
    class Meta:
        model = CustomUser
        fields = ('name','designation','profile_image','password1','password2')

              
    
class CreateTransactionForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('dealer','amount','payment_mode','remark')
        labels = { 
            'payment_mode': 'Payment Mode', 
        }          
    
class UpdateTransactionForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('dealer','payment_mode','remark','amount')
        labels = { 
            'payment_mode': 'Payment Mode', 
        }   



class PerformaInvoiceCreationForm(forms.ModelForm):
    class Meta:
        model = PerformaInvoice
        fields = ( 'party_name','address','gst_number','mobile','state') 
      
class PerformaInvoiceUpdateForm(forms.ModelForm):
    class Meta: 
        model = PerformaInvoice
        fields = ( 'party_name','address','gst_number','mobile','state') 

     
class PerformaInvoiceProductForm(forms.ModelForm):
    class Meta: 
        model = PerformaInvoiceItem
        fields = ('product','quantity','rate','gst_percent','taxable_amount','gst_amount','total_amount')
        widgets = {
            'product': forms.Select(attrs={'onchange': 'get_details()'}), 
            'quantity': forms.TextInput(attrs={'oninput': 'generate_amount()'}), 
            'rate': forms.TextInput(attrs={'oninput': 'generate_amount()'}), 
            'gst_percent': forms.TextInput(attrs={'oninput': 'generate_amount()','readonly': True}), 
            'gst_amount': forms.TextInput(attrs={'readonly': True}), 
            'taxable_amount': forms.TextInput(attrs={'readonly': True}), 
            'total_amount': forms.TextInput(attrs={'readonly': True}), 
            # 'rate': forms.TextInput(attrs={'readonly': True}), 
        }
        labels = { 
            'rate': 'Basic Amount',
            'taxable_amount': 'Taxable Amount', 
            'gst_percent': 'GST %', 
            'gst_amount': 'GST Amount', 
            'total_amount': 'Total Amount', 
        } 
