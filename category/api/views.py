from category.models import Category

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CategorySerializer,CreateCategorySerializer

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_category(request):
    if request.method == 'POST':
        user = request.user
    data = request.data
    _mutable = data._mutable
    data._mutable = True
    data['creator'] = user.pk
    data._mutable = _mutable
    serializer = CreateCategorySerializer(data=data)

    data = {}

    if serializer.is_valid():
        serializer.save()
        data['response'] = 'Success'
        return Response(data=data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)