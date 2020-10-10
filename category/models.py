from django.db import models
from django.utils.text import slugify

from account.models import Account

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(max_length=60,verbose_name='slug',unique=True,editable=False)
    tag = models.CharField(max_length=50,verbose_name='tag',unique=True)
    created_date = models.DateTimeField(auto_now_add=True,verbose_name='created_date')
    creator = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.tag

    def get_unique_slug(self):
        slug = slugify(self.tag.replace('ı','i'))
        return slug

    def save(self,*args,**kwargs):
        self.slug = self.get_unique_slug()
        return super(Category,self).save(*args,**kwargs)
