from rest_framework import serializers
from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')
    post = serializers.SerializerMethodField('get_post_description')
    class Meta:
        model = Comment
        fields = ['text','author','post']

    def get_author_name(self,comment):
        author = comment.author.username
        return author

    def get_post_description(self,comment):
        post = comment.post.description
        return post

#Update comment serializer

#Createcomment serializer fakat çalışmıyor aq
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text','author','post']

    


