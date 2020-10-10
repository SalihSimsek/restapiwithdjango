from account.models import Account
from rest_framework import serializers
from post.api.serializers import PostSerializer

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['email','username','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match'})

        user.set_password(password)
        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):
    follow_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    posts = PostSerializer('posts',many=True)
    class Meta:
        model = Account
        fields = ['pk','email','username','follow_count','follower_count','image','posts']

    def get_follow_count(self,obj):
        return obj.follow.count()

    def get_follower_count(self,obj):
        return obj.follower.count()
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
