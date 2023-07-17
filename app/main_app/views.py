from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, TagUser, FollowingUser
###
from django.http import HttpResponse
from main_app.forms import CustomUserCreationForm


### RENDERING ENDPOINTS ###

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


@login_required
def home(request):
    name = "";
    try:
        name = request.user.username;
        context = {
            'username':name, 
        };
        return render(request, "main_app/home_page.html", context);
    except Exception as e:
        print(e);
        return HttpResponse('An error has ocurred', status=404);


def create_post(request):
    if request.method == 'GET':
        return HttpResponse('create_post');
    else:
        return HttpResponse('Unsupported method', status=405);

def edit_post(request, id):
    if request.method == 'GET':
        return HttpResponse('edit post' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

def view_post(request, id):
    if request.method == 'GET':
        return HttpResponse('view post' + str(id));
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def view_account(request, username):
    if request.method == 'GET':
        try:
            logged_user = request.user;
            target_user = CustomUser.objects.get(username=username);
            tags = TagUser.objects.filter(user_id__id=target_user.id).values('tag_id__name');
            
            print(target_user.username);
            print(logged_user.username);


            context = {
                        'name':target_user.first_name,
                        'target_username':target_user.username,
                        'logged_username':logged_user.username,
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
        try:
            
            target_user = CustomUser.objects.get(username=username);

            target_user_name = target_user.first_name;

            target_id = target_user.id;

            follower_users = FollowingUser.objects.filter(follower_user_id__id=target_id).values('target_user_id__first_name');

            target_users = FollowingUser.objects.filter(target_user_id__id=target_id).values('follower_user_id__first_name');

            context = {
                'target_user_name': target_user_name,
                'follower_users': follower_users,
                'target_users':target_users
            }

            return render(request, 'main_app/social.html', context);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=404);
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


def search(request):
    if request.method == 'GET':
        return HttpResponse('search');
    else:
        return HttpResponse('Unsupported method', status=405);

### ////////////////// ###