from django.db import models

from account.models import Account
from post.models import Post

# Create your models here.
class Comment(models.Model):
    text = models.TextField()
    created_date = models.DateTimeField(verbose_name='created_date',auto_now_add=True)
    #Posta bağlanacak
    post = models.ForeignKey(Post,verbose_name='post',on_delete=models.CASCADE,related_name='comments')
    #User veya profile bağlanacak
    author = models.ForeignKey(Account,verbose_name='author',on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username+"-"+self.text

    # def children(self):
    #     return Comment.objects.filter(parent=self)

    # @property
    # def is_parent(self):
    #     if self.parent is not None:
    #         return False
    #     return True

