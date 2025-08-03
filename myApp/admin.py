from django.contrib import admin
from myApp.models import CustomUser, ProfileMedia, Tag

# Register your models here.

admin.site.register(Tag)
admin.site.register(CustomUser)
admin.site.register(ProfileMedia)
