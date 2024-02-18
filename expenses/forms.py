from django import forms

from django.contrib.auth.models import User
from .models import Expense, Activity


class AddParticipantForm(forms.ModelForm):
    participant = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Activity
        fields = []


    def clean(self):
        cleaned_data = super().clean()

        activity = self.instance
        participant = self.cleaned_data.get('participant')

        if participant in activity.participants.all():
            raise forms.ValidationError('User already in activity')

        return cleaned_data

    
    def save(self):
        activity = self.instance
        participant = self.cleaned_data.get('participant')
        activity.participants.add(participant)
        activity.save()


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['payer', 'title', 'amount']


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount should be positive number')
        rounded_amount = round(amount, 2)
        return rounded_amount
    

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name']

    
        
        
        
    

    