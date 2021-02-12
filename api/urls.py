from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet


router = DefaultRouter()
router.register('posts', PostViewSet, basename='PostViewSet')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='CommentViewSet')
router.register('follow', FollowViewSet, basename='FollowViewSet')
router.register('group', GroupViewSet, basename='GroupViewSet')


urlpatterns = [
    path('', include(router.urls)),
    #path('follow/', FollowViewSet.as_view()),
    #path('group/', GroupViewSet.as_view())
]
