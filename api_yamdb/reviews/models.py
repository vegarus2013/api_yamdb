from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE_CHOISE = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=255,
        choices=ROLE_CHOISE,
        default='user',
        blank=True,
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )

    @property
    def is_admin(self):
        return any(
            [self.role == 'admin', self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genres, through='GenreTitle')
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='title')

    def __str__(self):
        return self.name


class Reviews(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    reviews = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class GenreTitle(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'
