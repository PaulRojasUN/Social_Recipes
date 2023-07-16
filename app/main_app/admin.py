from django.contrib import admin
from .models import CustomUser, Tag, TagUser

admin.site.register(CustomUser);
admin.site.register(Tag);
admin.site.register(TagUser);

