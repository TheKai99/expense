from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
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

    selected_category = request.GET.get('category')

    if selected_category:

        expenses = expenses.filter(category = selected_category)


    check = expenses.aaggregate(

    )

    return render(request , 'home.html' , {'expenses':expenses , 'selected_category':selected_category})


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