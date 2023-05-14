from django import forms
from sharedapp.models import User
from tenantapp.models import Product

class RegisterForm(forms.ModelForm):
    company_name = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name',  'company_name']
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }
    def clean(self):
            cleaned_data = super(RegisterForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("password2")

            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )   
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price']