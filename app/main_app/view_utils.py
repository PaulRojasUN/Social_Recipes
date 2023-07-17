from django.http import HttpResponse
from .models import FollowingUser
from django.db.models import Q

def prepare_view_account(request, target_username):
    if request.method == 'GET':
        try:
            follower_username = request.user.username;
            
            if (follower_username==target_username):
                return HttpResponse('Cannot follow yourself', status=250);

            already_following = FollowingUser.objects.filter(Q(follower_user_id__username=follower_username)&
                                                             Q(target_user_id__username=target_username)).exists();
            
            if not already_following:
                return HttpResponse('Not following', status=251);
            else:
                return HttpResponse('Already following', status=252);

        except Exception as e:
            print(e);
            return HttpResponse('Wrong request', status=400);
    else:
        return HttpResponse('Unsupported method', status=405);