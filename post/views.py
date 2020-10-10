from django.shortcuts import render
from .models import Post
from account.models import Account
# Create your views here.

def index(request):
    posts = Post.objects.all()
    context = {
        'posts':posts,
    }
    return render(request,'post/index.html',context)


