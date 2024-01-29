from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.urls import reverse

from .models import Activity, Expense
from .forms import ExpenseForm



def dashboard(request):
    return render(request, 'expenses/dashboard.html')


def activity(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    participants = activity.participants.all()
    expenses = activity.expenses.all()

    participants_number = participants.count()
    total_amount = round(expenses.aggregate(Sum('amount'))['amount__sum'], 2)
    amount_per_participant = round(total_amount / participants_number, 2)


    form = ExpenseForm()
    form.fields['payer'].queryset = participants
    
    

    context = {
        'activity': activity,
        'participants': participants,
        'expenses': expenses,
        'participants_number': participants_number,
        'total_amount': total_amount,
        'amount_per_participant': amount_per_participant,
        'form': form,
    }

    return render(request, 'expenses/activity.html', context)


def balance(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    participants_number = activity.participants.count()
    total_amount = activity.expenses.aggregate(Sum('amount'))['amount__sum']
    amount_per_participant = round(total_amount / participants_number, 2)

    amount_spent = Sum('expense__amount', default=0, filter=Q(expense__activity=activity_id))
    participants = activity.participants.annotate(balance=amount_spent - amount_per_participant)
  
    creditors = sorted([[participant.username, participant.balance] for participant in participants if participant.balance > 0], key=lambda x: x[1], reverse=True)
    debtors = sorted([[participant.username, participant.balance] for participant in participants if participant.balance < 0], key=lambda x: x[1])

    reimbursements = []

    while creditors and debtors:
        creditor, creditor_balance = creditors[-1]
        debtor, debtor_balance = debtors[-1]

        amount = min(-debtor_balance, creditor_balance)
        reimbursements.append((debtor, creditor, amount))
        creditors[-1][1] -= amount
        debtors[-1][1] += amount

        if creditors[-1][1] == 0:
            creditors.pop()      
        if debtors[-1][1] == 0:
            debtors.pop()
           
    context = {
        'activity': activity,
        'participants': participants,
        'reimbursements': reimbursements,
    }
    return render(request, 'expenses/balance.html', context)


def create_expense(request, activity_id):
    if request.method == 'POST':
        activity = get_object_or_404(Activity, pk=activity_id)
        expense = Expense(activity=activity)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(reverse('expenses:activity', args=[activity_id]))
        else:
            print(form.errors)


def expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    payer = expense.payer
    activity = expense.activity

    context = {
        'expense': expense,
        'payer': payer,
        'activity': activity,
    }
    return render(request, 'expenses/expense.html', context)