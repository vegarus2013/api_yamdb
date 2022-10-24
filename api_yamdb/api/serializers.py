import datetime as dt
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import User, Categories, Genres, Titles


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {'Выберите другой username'})
        return data


class UserAccessSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'bio', 'email', 'role']


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['name', 'slug']


class GenreSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ['name', 'slug']


class TitleSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(),
                                            slug_field='slug',)
    genre = serializers.SlugRelatedField(queryset=Genres.objects.all(),
                                         slug_field='slug',
                                         many=True)

    class Meta:
        model = Titles
        # TODO Добавить поле рейтинг, которое будет высчитываять
        # как среднее арифмитическое из всех обзоров на данное произведение
        fields = ['category', 'genre', 'name', 'year', 'description']

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть в будущем'
            )
        return value
