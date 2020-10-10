from django.urls import path
from .views import *

app_name='categoryapi'
urlpatterns = [
    path('categories/',all_categories,name='categories'),
    path('create/',create_category,name='create'),
]