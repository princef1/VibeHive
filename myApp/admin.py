from django.contrib import admin
from myApp.models import CustomUser, FriendRequest, Friendship, Location, ProfileMedia, Tag, UserProfile

# Register your models here.

admin.site.register(Location)
admin.site.register(Tag)
admin.site.register(CustomUser)
admin.site.register(ProfileMedia)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Friendship)

