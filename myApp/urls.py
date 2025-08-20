from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =   [
    path('',views.landingpage, name = 'landingpage'),
    path('register/',views.signup, name = 'signup'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout, name = 'logout'),
    path('setup_profile/',views.setup_profile, name = 'setup_profile'),
    path('edit_profile/',views.edit_profile, name = 'edit_profile'),
    path('feed/',views.feed, name = 'feed'),
    path('friend-requests/',views.friendrequest, name = 'friend_requests'),
    path('friend-request/respond/<int:request_id>/<str:action>/', views.respond_friend_request, name='respond_friend_request'),
    path('send-request/<str:user_name>/', views.send_friend_request, name='send_friend_request'),
    path('cancel-friend-request/<str:user_name>/',views.cancel_friend_request, name = 'cancel_friend_request'),
    path('unfriend/<str:user_name>/',views.unfriend, name = 'unfriend'),
    path('friends/', views.friend_list, name='friend_list'),
    path('friends/<str:user_name>/', views.user_friend_list, name='user_friend_list'),
    path('next/<str:user_name>/', views.next_user, name='next_user'),
    path('profile/<str:user_name>/', views.profile, name='profile'),
    path('search/', views.search_user, name='search_user'),
    path('chat/', views.chat, name='chat'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
