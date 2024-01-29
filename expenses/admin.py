from django.contrib import admin
from .models import Activity, Expense

# Register your models here.

admin.site.register([Activity, Expense])