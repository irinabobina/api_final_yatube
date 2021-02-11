from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter
from .models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(ModelViewSet):
    """
    Получить список всех записей, отфильтровать по группе - доступно всем.
    Создать новую запись - только для зарегистрированных
    пользователей.
    Изменить или удалить запись - только для зарегистрированных
    пользователей и только в отношении своих комментариев.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PostFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,)


class CommentViewSet(ModelViewSet):
    """
    Получить список всех комментариев к конкретной записи - доступно всем.
    Создать новый комментарий - только для зарегистрированных
    пользователей.
    Изменить или удалить комментарий - только для зарегистрированных
    пользователей и только в отношении своих комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post_id=post.pk,
        )


class FollowList(generics.ListCreateAPIView):
    """
    Получить список всех подписок и возможность отфильтровать их
    по подписчику или тому, на кого подписались - доступно всем.
    Создать новую подписку - доступно только зарегистрированному
    пользователю и только для себя.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,)


class GroupList(generics.ListCreateAPIView):
    """
    Получить список всех групп - доступно всем.
    Создать новую группу - доступно зарегистрированным пользователям.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
