from django.http import HttpResponse
from .models import FollowingUser, CustomUser
from django.db.models import Q
from django.shortcuts import redirect

def add_following(request):
    if request.method == 'POST':
        try:
            follower_username = request.POST['follower_user'];   
            target_username = request.POST['target_user'];   
            
            if (follower_username == target_username):
                return HttpResponse('Sorry, that is not allowed', status=400);

            already_following = FollowingUser.objects.filter(Q(follower_user_id__username=follower_username)&
                                                             Q(target_user_id__username=target_username)).exists();

            if not (already_following):
                follower_user = CustomUser.objects.get(username=follower_username);

                target_user = CustomUser.objects.get(username=target_username);

                FollowingUser.objects.create(follower_user_id=follower_user, target_user_id=target_user);

            
            else:
                obj = FollowingUser.objects.get(Q(follower_user_id__username=follower_username)&
                                                Q(target_user_id__username=target_username));
                
                obj.delete();

            return redirect(request.META['HTTP_REFERER']);
        except Exception as e:
            print(e);
            return HttpResponse('An error has ocurred', status=404);    
    else:
        return HttpResponse('Unsupported method', status=405);