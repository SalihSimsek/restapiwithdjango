from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,LoginForm,AccountUpdateForm
from .models import Account
from django.contrib.auth import authenticate,login,logout
# Create your views here.

def create_account(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        # follow = Follow(uprofile=user)
        # follower = Follower(uprofile=user)
        # follower.save()
        # follow.save()
        #Kullanıcı burada log edilmeli ve userprofile forma yönlendirilmeli
        return redirect('post:index')
    context = {
        'form':form,
        'title':'Kaydol',
    }
    return render(request,'account/form.html',context)

def login_account(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('post:index')
    context = {
        'form':form,
        'title':'Giriş Yap'
    }
    return render(request,'account/form.html',context)

def update_account(request):
    if not request.user.is_authenticated:
        return redirect('account:login')
    context={}

    if request.POST:
        form = AccountUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('post:index')
    else:
        form = AccountUpdateForm(
            initial = {
                'email' : request.user.email,
                'username' : request.user.username,
            }
        )
    context['account_form']=form
    return render(request,'account/form.html')
 
def logout_account(request):
    logout(request)
    return redirect('post:index')

def account_detail(request,username):
    account = get_object_or_404(Account,username=username)
    follow = account.follow.all()
    follower = account.follower.all()
    isActive=True
    
    if request.user in follower:
        isActive=False

    context = {
        'user':account,
        'follower':follower,
        'follow':follow,
        'isActive':isActive,
    }
    return render(request,'account/account_detail.html',context)

def follow_user(request,username):
    req_user = request.user
    account = get_object_or_404(Account,username=username)
    req_user.follow.add(account)
    return redirect('account:account_detail',username=account)

def unfollow_user(request,username):
    req_user = request.user
    account = get_object_or_404(Account,username=username)
    req_user.follow.remove(account)
    return redirect('account:account_detail',username=account)