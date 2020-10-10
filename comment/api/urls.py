from django.urls import path

from .views import *

app_name='comment_api'
urlpatterns = [
    path('comments/',get_all_comments,name='get_all_comments'),
    path('<slug>/postcomment/',get_posts_comments,name='get_posts_comments'),
    path('<int:pk>/delete/',delete_comment,name='delete_comment'),
    path('<slug>/addcomment/',add_comment,name='add_comment')
]