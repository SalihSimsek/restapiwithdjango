from django.urls import path
from .views import *
# ,account_view,update_account_view,change_password_view

app_name='account_api'
urlpatterns = [
    path('login/',ObtainAuthTokenView.as_view(),name='login'),
    path('register/',registration_view,name='register'),
    path('detail/',account_view,name='detail'),
    path('update/',update_account,name='update'),
    path('logout/',Logout.as_view(),name='logout'),
    path('changepassword/',ChangePasswordView.as_view(),name='change_password'),
    path('<username>/detail/',account_detail_view,name='acccount_detailview'),
    ##Follow url
    path('<username>/follow/',add_follow,name='add_follow'),
    path('<username>/unfollow/',remove_follow,name='remove_follow'),
    #Filter
    path('list',ApiUserListView.as_view(),name='search_user'),
]