from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
###
from django.http import HttpResponse


### Registration ###

@login_required
def home(request):
    name = "";
    try:
        name = request.user.username;
        print(name)
    except Exception as e:
        print(e);
    return render(request, "registration/home_page.html", {name:name})
 
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


###  ///////////////////////// ###


def create_recipe(request):
    if request.method == 'GET':
        return HttpResponse('create_recipe');
    else:
        return HttpResponse('Unsupported method', status=405);

def edit_recipe(request, id):
    if request.method == 'GET':
        return HttpResponse('edit recipe' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def view_recipe(request, id):
    if request.method == 'GET':
        return HttpResponse('view recipe' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def view_account(request, id):
    if request.method == 'GET':
        return HttpResponse('view account' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def edit_account(request, id):
    if request.method == 'GET':
        return HttpResponse('edit account' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def social(request, id):
    if request.method == 'GET':
        return HttpResponse('social' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def filter(request):
    if request.method == 'GET':
        
        obj = request.GET;

        for i in obj:
            print(str(i) + ":" + str(obj[i]));
            
        return HttpResponse('filter');
    else:
        return HttpResponse('Unsupported method', status=405);

