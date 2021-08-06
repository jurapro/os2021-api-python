from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .exceptions import CafeValidationAPIException, CafeAPIException
from .models import User, WorkShift
from .permissions import IsAuthenticated, IsAdmin
from .serializers import UserSerializer, LoginSerializer, UserCreateSerializer, WorkShiftSerializer


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if not (serializer.is_valid()):
        raise CafeValidationAPIException(message='Validation error',
                                         code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                         errors=serializer.errors)
    try:
        user = User.objects.get(login=serializer.data['login'], password=serializer.data['password'])
    except User.DoesNotExist:
        raise CafeAPIException(message='Authentication failed',
                               code=status.HTTP_401_UNAUTHORIZED)

    user.api_token = get_random_string(length=32)
    user.save()

    response = {
        'date': {
            'user_token': user.api_token,
        }
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def logout(request):
    user = User.get_auth_user(request)
    user.api_token = None
    user.save()
    response = {
        'date': {
            'message': 'Logout',
        }
    }
    return Response(response, status=status.HTTP_200_OK)


class UserList(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)

        if not (serializer.is_valid()):
            raise CafeValidationAPIException(message='Validation error',
                                             code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                             errors=serializer.errors)
        serializer.save()
        response = {
            'data': {
                'id': serializer.instance.id,
                'status': 'created'
            }
        }
        return Response(response, status=status.HTTP_201_CREATED)


class WorkShiftViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = WorkShift.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = WorkShiftSerializer(data=request.data)
        if not (serializer.is_valid()):
            raise CafeValidationAPIException(message='Validation error',
                                             code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                             errors=serializer.errors)
        serializer.save()
        return Response(
            serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def open(self, request, pk=None):
        return Response({
            'id': pk,
            'start': self.get_object().start
        })
