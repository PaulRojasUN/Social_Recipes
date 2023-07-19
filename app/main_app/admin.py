from django.contrib import admin
from .models import CustomUser, Tag, TagUser, FollowingUser, ClassifiedTag, UnclassifiedTag

admin.site.register(CustomUser);
admin.site.register(Tag);
admin.site.register(ClassifiedTag);
admin.site.register(UnclassifiedTag);
admin.site.register(TagUser);
admin.site.register(FollowingUser);

