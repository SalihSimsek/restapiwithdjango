from django.urls import path
from .views import *

app_name='post_api'
urlpatterns = [
    path('posts/',post_view,name='post_view'),
    path('onlyfollowposts/',only_follow_users_posts,name='only_follow_users_posts'),
    path('<slug>/update/',update_post,name='update_post'),
    path('create/',create_post,name='create_post'),
    path('<slug>/delete/',delete_post,name='delete_post'),
    path('<slug>/detail/',post_detail,name='post_detail'),
    path('<slug>/like/',like_post,name='like_post'),
    path('<slug>/dislike/',dislike_post,name='dislike_post'),
    #User liked post
    path('p/likedposts/',get_all_liked_post,name='liked'),
    path('<slug>/addfavorite/',add_favorite_post,name='add_favorite_post'),
    path('p/getfavposts/',get_favorite_posts,name='get_favorite_posts'),
]