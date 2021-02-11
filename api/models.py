from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify


User = get_user_model()


class Group(models.Model):
    """
    Модель для хранения данных о сообществах.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='название',
    )
    slug = models.SlugField(
        unique=True, blank=True
    )
    description = models.TextField(
        verbose_name='описание',
    )

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'

    #  Автоматическое создание слага из названия сообщества (title)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    """
    Модель для хранения данных о постах.
    """
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='сообщество',
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    Модель для хранения данных о комментариях к постам.
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='комментируемая запись',
    )
    text = models.TextField(
        verbose_name='текст комментария',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата добавления',
    )


class Follow(models.Model):
    """
    Модель для хранения данных о подписчиках.
    """
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'подписчик'
        verbose_name_plural = 'подписчики'
        unique_together = ('user', 'following',)

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
