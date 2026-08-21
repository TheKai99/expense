from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum , Count

# Create your views here.

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Expense
from .service import generate_spending_summary


@login_required
def ai_summary(request):
    expenses = Expense.objects.filter(user=request.user)

    category_summary = list(
        expenses.values('category').annotate(total=Sum('amount'), count=Count('id'))
    )

    summary_text = generate_spending_summary(category_summary)  # no try/except temporarily

    return JsonResponse({'summary': summary_text})


@login_required(login_url='login_page')
def home(request):

    if request.method == 'POST':


        data = request.POST

        amount = data.get('amount')
        category = data.get('category')
        description = data.get('description')

        if not amount or not category:
            messages.error(request , 'fill all the requirements')
            return redirect('home')

        try:

            Expense.objects.create(
            
                        user = request.user,
                        amount = amount,
                        category = category,
                        description = description,
            
                    )
            messages.success(request , 'Expense added successfully')
        except(ValueError , TypeError):

            messages.error(request , 'Invalid amount entered')

        return redirect('home')

    
    expenses = Expense.objects.filter(user = request.user)


    recent_expenses = expenses.order_by('-date')[:5]  # last 5 added

     
    # Fot total expense and totol count

    check = expenses.aggregate(

        total = Sum('amount'),
        count = Count('id'),
    )

    total_expense = check['total'] or 0

    expense_count = check['count']

    # categories wise data info

    category_data = (

        expenses.values('category').annotate(total = Sum('amount') , count = Count('id')).order_by('-total')

    )

    if category_data:
       max_total = max(item['total'] for item in category_data)
       for item in category_data:
          item['percent'] = round((item['total'] / max_total) * 100) if max_total else 0

     # filter by category
    
    selected_category = request.GET.get('category')
    
    if selected_category:
        expenses = expenses.filter(category = selected_category)


    return render(request , 'home.html' , {'expenses':expenses , 'selected_category':selected_category ,
                                            'total_expense':total_expense , 'expense_count':expense_count,
                                            'category_data':category_data , 
                                            'recent_expenses': recent_expenses})


def delete(request , id):

    queryset = Expense.objects.get(id = id)
    queryset.delete()
    return redirect('home')


def update(request , id):

    queryset = Expense.objects.get(id = id)

    if request.method == 'POST':

        data = request.POST

        amount = data.get('amount')
        category = data.get('category')
        description = data.get('description')

        queryset.amount = amount
        queryset.category = category
        queryset.description = description

        queryset.save()

        return redirect('home')

    return render(request , 'update.html' , {'queryset':queryset})