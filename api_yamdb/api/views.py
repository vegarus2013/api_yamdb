from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdmin, IsAdminModeratorAuthorOrReadOnly,
                          IsAdminUserOrReadOnly)
from .serializers import (CategorySerializers, CommentSerializer,
                          GenreSerializers, ReviewSerializer, SignupSerializer,
                          TitleSerializers, UserAccessSerializer,
                          UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    is_email = User.objects.filter(email=email).exists()
    is_username = User.objects.filter(username=username).exists()
    if is_email or is_username:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user, code_created = User.objects.get_or_create(
        email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подтвержения для завершения регистрации',
        f'Ваш код для получения JWT токена {user.confirmation_code}',
        settings.CODE_EMAIL,
        [email],
        fail_silently=True,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = UserAccessSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    search_fields = ('name',)
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')
    serializer_class = TitleSerializers
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
