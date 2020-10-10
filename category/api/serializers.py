from rest_framework import serializers
from category.models import Category
from post.api.serializers import PostSerializer

class CategorySerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField('get_creator_username')
    posts = PostSerializer(many=True)
    class Meta:
        model = Category
        fields = ['tag','creator','posts']
    
    def get_creator_username(self,category):
        creator = category.creator.username
        return creator

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['tag','creator']
