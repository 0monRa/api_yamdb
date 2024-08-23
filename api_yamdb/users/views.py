import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import views, viewsets

from .permissions import (
    AdministratorPermission,
    AuthenticatedPermission,
)
from .serializers import (
    AdminSerializer,
    SignupSerializer,
    UserSerializer,
)

UserModel = get_user_model()


@api_view(['POST'])
def auth_signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        send_mail(
            subject='Confirmation Code',
            message=str(user.confirmation_code),
            from_email='from@example.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def auth_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    if not username:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(UserModel, username=username)

    try:
        confirmation_code = uuid.UUID(confirmation_code)
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if user.confirmation_code == confirmation_code:
        refresh = RefreshToken.for_user(user)
        data = {'token': str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    lookup_field = 'username'
    serializer_class = AdminSerializer
    permission_classes = (AdministratorPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        for key in ('username', 'email'):
            data = {key: serializer.validated_data.get(key)}
            user = UserModel.objects.filter(**data)
            if user.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class MeViewSet(views.APIView):
    permission_classes = (AuthenticatedPermission,)

    def get(self, request):
        user = get_object_or_404(
            UserModel,
            username=request.user.username
        )
        serializer = AdminSerializer(user)
        self.check_object_permissions(request, user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(
            UserModel,
            username=request.user.username
        )
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)
