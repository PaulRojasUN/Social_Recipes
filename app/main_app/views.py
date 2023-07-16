from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, TagUser
###
from django.http import HttpResponse
from main_app.forms import CustomUserCreationForm

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
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
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

@login_required
def view_account(request, username):
    if request.method == 'GET':
        try:
            user = CustomUser.objects.get(username=username);
            tags = TagUser.objects.filter(user_id__id=user.id).values('tag_id__name');
            
            context = {'name':user.first_name,
                        'username':user.username,
                        'tags':tags,
                        };
            return render(request, 'main_app/view_account.html', context);
        except Exception as e:
            print(e);
            return HttpResponse('User was not found', status=404);
    else:
        return HttpResponse('Unsupported method', status=405);

def edit_account(request, username):
    if request.method == 'GET':
        return HttpResponse('edit account ' + str(username));
    else:
        return HttpResponse('Unsupported method', status=405);

def social(request, username):
    if request.method == 'GET':
        return HttpResponse('social ' + str(username));
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

