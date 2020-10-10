from django.urls import path,reverse_lazy
from .views import create_account,login_account,logout_account,update_account,account_detail,follow_user,unfollow_user

app_name='account'
urlpatterns = [
    path('register/',create_account,name='create'),
    path('login/',login_account,name='login'),
    path('logout/',logout_account,name='logout'),
    path('<username>/update/',update_account,name='update'),
    path('<username>/',account_detail,name='account_detail'),
    path('<username>/follow/',follow_user,name='follow_user'),
    path('<username>/unfollow/',unfollow_user,name='unfollow_user')    
]