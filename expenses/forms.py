from django import forms

from django.contrib.auth.models import User
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['payer', 'amount', 'title']
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount should be positive number')
        rounded_amount = round(amount, 2)
        return rounded_amount
    
        
        
        
    

    