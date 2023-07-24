from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Subquery, OuterRef, Count


# Users
from .models import CustomUser, FollowingUser

# Tag
from .models import TagUser

# Post
from .models import Post, PostLike

# Access 
from .models import priviliged_access, admin_access

###
from django.http import HttpResponse, JsonResponse
from main_app.forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test


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

@login_required
def create_post(request):
    if request.method == 'GET':
        return render(request, 'main_app/create_post.html');
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def edit_post(request, id):
    if request.method == 'GET':

        try:
            logged_in_user = request.user;

            if not logged_in_user.groups.first().name == 'admin':
            
                if not Post.objects.filter(Q(id=id) & Q(author_user_id=logged_in_user)).exists():                
                    return HttpResponse('Forbidden', status=403);  

            context = {
                'post_id':id,
            };
                
            return render(request, 'main_app/edit_post.html', context);
                  
        except Exception:
            return HttpResponse('Something went wrong', status=405);
    
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def view_post(request, id):
    if request.method == 'GET':
        try:
            if not Post.objects.filter(id=id).exists():
                raise Exception('Such post does not exist');

            user = request.user;

            post = Post.objects.get(id=id);

            post_owner = post.author_user_id;

            is_hidden = True;

            if not user.groups.first().name == 'admin':
                is_owner = user == post_owner;
                if is_owner:
                    is_hidden = False;
                if (post.visibility == 2):
                    if not is_owner:
                        return HttpResponse('Forbidden', status=403);
                elif (post.visibility == 1):
                    if FollowingUser.objects.filter(Q(follower_user_id=user)&Q(target_user_id=post_owner)).exists():
                        return HttpResponse('Forbidden', status=403);
            else:
                is_hidden = False;

            context = {
                'post_id':post.id,
                'post_owner_name':post_owner.first_name,
                'is_hidden':is_hidden,
            }

            return render(request, 'main_app/view_post.html', context); 
                    
        except Exception as e:
            print(e);
            return HttpResponse('Bad Request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def view_account(request, username):
    if request.method == 'GET':
        try:
            logged_user = request.user;
            target_user = CustomUser.objects.get(username=username);
            tags = TagUser.objects.filter(user_id__id=target_user.id).values('tag_id__name');

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
        try:
            logged_user = request.user;
            target_user = CustomUser.objects.get(username=username);

            own_account = logged_user.id == target_user.id;

            is_admin = logged_user.groups.first().name=='admin';

            if (own_account or is_admin):
                tags = TagUser.objects.filter(user_id__id=target_user.id).values('tag_id__name');


                context = {
                            'name':target_user.first_name,
                            'target_username':target_user.username,
                            'tags':tags,
                            };
                return render(request, 'main_app/edit_account.html', context);
        
            else:
                return HttpResponse('Sorry, you cannot access this site', status=403);
        except Exception as e:
            print(e);
            return HttpResponse('User was not found', status=404)
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def social(request, username):
    if request.method == 'GET':
        try:
            
            target_user = CustomUser.objects.get(username=username);

            target_user_name = target_user.first_name;

            target_id = target_user.id;

            follower_users = FollowingUser.objects.filter(follower_user_id__id=target_id).values('target_user_id__first_name', 'target_user_id__username');

            target_users = FollowingUser.objects.filter(target_user_id__id=target_id).values('follower_user_id__first_name','follower_user_id__username');

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

@login_required
def filter(request):
    if request.method == 'GET':    
        try:
            obj = request.GET;

            username = request.user.username,
            print(type(request.user.username))
            print("sdsa")
            context = {
                'par1':obj['par1'],
                'username':str(username[0]),#str(username),
            }

            return render(request, 'main_app/filter.html', context);
        except Exception as e:
            print(e);
            return HttpResponse('Bad Request', status=400);    
        
    else: 
        return HttpResponse('Unsupported method', status=405);

@login_required
def search(request):
    if request.method == 'GET':
        return render(request, 'main_app/search.html');
    else:
        return HttpResponse('Unsupported method', status=405);

@login_required
def tags_manager(request):
    if request.method == 'GET':
        return HttpResponse('Tags Manager');
    else:
        return HttpResponse('Unsupported method', status=405);


@user_passes_test(admin_access)
def admin_manage_users(request):
    if request.method == 'GET':
        return render(request, 'main_app/admin_manage_users.html');
    else:   
        return HttpResponse('Unsupported method', status=405);

@user_passes_test(priviliged_access)
def tags_management(request):
    if request.method == 'GET':
        return render(request, 'main_app/tags_management.html');
    else:
        return HttpResponse('Unsupported method', status=405);

@user_passes_test(priviliged_access)
def ingredients_management(request):
    if request.method == 'GET':
        return render(request, 'main_app/ingredients_management.html');
    else:
        return HttpResponse('Unsupported method', status=405);

### ////////////////// ###