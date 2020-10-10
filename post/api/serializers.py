from post.models import Post
from rest_framework import serializers
from comment.api.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_username_from_author')
    video = serializers.SerializerMethodField('validate_video_url')
    like_count = serializers.SerializerMethodField('get_like_count')
    dislike_count = serializers.SerializerMethodField('get_dislike_count')
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ['slug','description','video','created_date','author','like_count','likes','dislike_count','dislikes','favorites','comments']

    def get_username_from_author(self,post):
        username = post.author.username
        return username

    def validate_video_url(self,post):
        video = post.video
        new_url = video.url
        if '?' in new_url:
            new_url = image.url[:image.url.rfind('?')]
        return new_url

    def get_like_count(self,obj):
        return obj.likes.count()

    def get_dislike_count(self,obj):
        return obj.dislikes.count()
    
    def create(self,validated_data):
        comments_data = validated_data.pop('comments')
        post = Post.objects.create(**validated_data)
        for comment_data in comments_data:
            Comment.objects.create(post=post,**comment_data)


##Post UpdateSerializer
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['description']

##Post CreateSerializer
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['video','description','author','created_date']

class LikePostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = Post
        fields = ['slug','video','author']

    def get_username_from_author(self,post):
        username = post.author.username
        return username