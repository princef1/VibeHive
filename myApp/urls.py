from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =   [
    path('',views.landingpage, name = 'landingpage'),
    path('register/',views.signup, name = 'signup'),
    path('login/',views.user_login, name = 'login'),
    path('logout/',views.user_logout, name = 'logout'),
    path('firstpage/',views.firstpage, name = 'firstpage'),
    path('card/', views.card_page, name='card_page'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
