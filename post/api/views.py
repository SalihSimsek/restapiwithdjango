from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import PostSerializer,PostUpdateSerializer,CreatePostSerializer,LikePostSerializer
from post.models import Post

from rest_framework.permissions import IsAuthenticated

#Tüm postlar geldi
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def post_view(request):
    posts = Post.objects.all().order_by('-created_date')
    serializer = PostSerializer(posts,many=True)
    return Response(serializer.data)

#Request userın takip ettiklerinin postları
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def only_follow_users_posts(request):
    user = request.user
    follows_user = user.follow.all()
    posts = Post.objects.filter(author_id__in=follows_user).order_by('-created_date')
    serializer = PostSerializer(posts,many=True)
    return Response(serializer.data)

#Post güncelleme
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_post(request,slug):
    data = {}
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if post.author != request.user:
        data['response'] = 'İzin haklarınız dışında işlem yaptınız'
        return Response(data=data)
    if request.method == 'PUT':
        serializer = PostUpdateSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Post update success'
            return Response(data=data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_post(request):
    if request.method == 'POST':
        data = request.data
        _mutable = data._mutable
        data._mutable = True
        data['author'] = request.user.pk
        data._mutable = _mutable
        serializer = CreatePostSerializer(data=data)

        data = {}

        if serializer.is_valid():
            post = serializer.save()
            data['response'] = 'Create Successfully'
            data['description'] = post.description
            data['slug'] = post.slug
            video_url = str(request.build_absolute_uri(post.video.url))
            if '?' in video_url:
                video_url = video_url[:video_url.rfind('?')]
            data['video'] = video_url
            return Response(data=data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_post(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExits:
        return Response(status = HTTP_404_NOT_FOUND)
    user = request.user
    if post.author != user:
        return Response({'response':'You dont have any permission to delete that'})
    
    if request.method == 'DELETE':
        operation = post.delete()
        data = {}
        if operation:
            data['success'] = 'Delete successful'
        else:
            data['failure'] = 'Delete Failed'
        return Response(data=data)
    
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def post_detail(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def like_post(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    user = request.user
    data = {}
    #Eğer user like butonuna tekrar tıklarsa geri al
    if request.method == 'POST':
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        if user in post.likes.all():
            post.likes.remove(user)
            data['response'] = 'Not Liked'
            return Response(data=data)
        else:
            post.likes.add(user)
            data['response'] = 'Liked'
            return Response(data=data)
    return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def dislike_post(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    user = request.user
    data = {}
    #Eğer user dislike butonuna tekrar tıklarsa geri al
    if request.method == 'POST':
        if user in post.likes.all():
            post.likes.remove(user)
        if user in post.dislikes.all():
            post.dislikes.remove(user)
            data['response'] = 'Not Disliked'
            return Response(data=data)
        else:
            post.dislikes.add(user)
            data['response'] = 'Disliked'
            return Response(data=data)
    return Response(status = status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_all_liked_post(request):
    user = request.user
    liked_post = user.liked.all()
    posts = Post.objects.filter(pk__in=liked_post).order_by('-created_date')
    serializer = LikePostSerializer(posts,many=True)
    return Response(serializer.data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def add_favorite_post(request,slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    data = {}
    user = request.user
    if request.method == 'POST':
        if user in post.favorites.all():
            user.favorited.remove(post)
            data['response'] = 'Remove fav'
            return Response(data=data)
        else:
            user.favorited.add(post)
            data['response'] = 'Succesfully added'
            return Response(data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_favorite_posts(request):
    user = request.user
    fav_posts = user.favorited.all()
    posts = Post.objects.filter(pk__in=fav_posts).order_by('-created_date')
    serializer = LikePostSerializer(posts,many=True)
    return Response(serializer.data)