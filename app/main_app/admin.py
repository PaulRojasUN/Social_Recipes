from django.contrib import admin
from .models import CustomUser, Tag, TagUser, FollowingUser

admin.site.register(CustomUser);
admin.site.register(Tag);
admin.site.register(TagUser);
admin.site.register(FollowingUser);

