import uuid
from django.db import models
from .validators import validate_file_extension

from account.models import Account
from category.models import Category

def upload_location(instance,filename):
    file_path = 'content/{owner_id}-{owner_username}/{filename}'.format(owner_id = str(instance.author.id),owner_username=str(instance.author.username),filename=filename)
    return file_path

def create_slug():
    slug = uuid.uuid4()
    slug = str(slug).replace('-','')
    if Post.objects.filter(slug=slug).exists():
        create_slug()
    return slug

# Create your models here.
class Post(models.Model):
    #Slug kayıt şekli eklenecek
    #Random slug oluşturulacak uuid kullanılacak
    slug = models.SlugField(default = create_slug,editable=False,unique=True,max_length=5)
    description = models.TextField()
    #Media tip sınırlandırması olacak
    #Sınırlama eklendi upload alanı koyulacak
    video = models.FileField(validators = [validate_file_extension],upload_to=upload_location,null=False,blank=False)
    #Like ve dislike alanları için liste tutucu oluşturulacak
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='created_date')
    updated_date = models.DateTimeField(auto_now=True,verbose_name='updated_date')
    author = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='posts',verbose_name='author')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,related_name='posts',verbose_name='category')
    likes = models.ManyToManyField(Account,related_name='liked',verbose_name='like')
    dislikes = models.ManyToManyField(Account,related_name='disliked',verbose_name='dislike')
    favorites = models.ManyToManyField(Account,related_name='favorited',verbose_name='favorites')

    def __str__(self):
        return self.description

    

# class Like(models.Model):
#     upost = models.OneToOneField(Post,verbose_name='Post',related_name='liked',on_delete=models.CASCADE)
#     like_user = models.ManyToManyField(Account,verbose_name='Like',related_name = 'liked_user')

# class Dislike(models.Model):
#     upost = models.OneToOneField(Post,verbose_name ='Post',related_name='dislike',on_delete=models.CASCADE)
#     dislike_user = models.ManyToManyField(Account,verbose_name='Dislike',related_name='disliked_user')
