from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="activities", related_query_name="activity")

    def __str__(self):
        return self.name


class Expense(models.Model):
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="expenses", related_query_name="expense")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="expenses", related_query_name="expense")
    title = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.title