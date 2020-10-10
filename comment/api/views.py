from comment.models import Comment
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommentSerializer,CreateCommentSerializer
from post.models import Post
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import IsAuthenticated


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_all_comments(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments,many=True)
    return Response(data=serializer.data)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_posts_comments(request,slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post_id=post)
    serializer = CommentSerializer(comments,many=True)
    return Response(serializer.data)

#Comment silme
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_comment(request,pk):
    comment = Comment.objects.get(pk=pk)
    user = request.user
    data = {}
    if user == comment.author:
        comment.delete()
        data['response'] = 'Silme işlemi başarılı'
        return Response(data=data)
    data['response'] = 'Yetki dışı işleminiz gerçekleştirilemedi'
    return Response(data=data)

#Comment send
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def add_comment(request,slug):
    if request.method=='POST':
        try:
            post = Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        data = request.data
        user = request.user
        _mutable = data._mutable
        data._mutable=True
        data['post'] = post.pk
        data['author'] = user.pk
        data._mutable = _mutable
        serializer = CreateCommentSerializer(data=data)

        data = {}

        if serializer.is_valid():
            comment = serializer.save()
            data['response'] = 'Create successfully'
            data['text'] = comment.text
            data['author'] = comment.author.username
            data['post'] = comment.post.slug
            return Response(data=data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        

#Comment update