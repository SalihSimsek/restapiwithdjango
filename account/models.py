from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

def upload_location(instance,filename):
    file_path = 'profileimage/{owner_id}-{owner_username}/{filename}'.format(owner_id = str(instance.id),owner_username = str(instance.username),filename=filename)
    return file_path

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractUser):
    first_name = models.CharField(max_length=20,verbose_name='first_name')
    last_name = models.CharField(max_length=20,verbose_name = 'last_name')
    email = models.CharField(max_length=60, verbose_name='email', unique=True)
    username = models.CharField(max_length=30, verbose_name='username', unique=True)
    biography = models.CharField(max_length=150,verbose_name='biography',blank=True,null=True)
    image = models.ImageField(upload_to=upload_location,default='default/default.jpeg',verbose_name='profile_image',blank=True,null=True)
    is_secret = models.BooleanField(default=False,verbose_name='is_secret')
    birthday = models.DateField(verbose_name='birthday',blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date_joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='last_login')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    follow = models.ManyToManyField('Account',related_name='follower',verbose_name='follows',blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()
    
    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True


# class Follower(models.Model):
#     uprofile = models.OneToOneField(Account,verbose_name='UserProfile',related_name='followers',on_delete=models.CASCADE,primary_key = True)
#     follower_user = models.ManyToManyField(Account,verbose_name='follower',blank=True)

#     def __str__(self):
#         return self.uprofile.username+" adlı kişinin takipçileri"

# class Follow(models.Model):
#     uprofile = models.OneToOneField(Account,verbose_name='UserProfile',related_name='follows',on_delete=models.CASCADE,primary_key=True)
#     follow_user = models.ManyToManyField(Account,verbose_name='follow',blank=True)

#     def __str__(self):
#         return self.uprofile.username+" adlı kişinin takip ettikleri"
