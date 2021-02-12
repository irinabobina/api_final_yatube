from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, User, Follow, Group



class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        #many=False,
        slug_field='username',
        #read_only=True,
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
        )
    following = serializers.SlugRelatedField(
        #many=False,
        slug_field='username',
        queryset=User.objects.all()
        )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = (
            UniqueTogetherValidator(queryset=Follow.objects.all(), fields=('user', 'following')),
        )

    def validate(self, data):
        if self.context['request'].method == "POST":
            if data.get('user') == data.get('following'):
                raise serializers.ValidationError('You cant follow yourself')
            return data
        #return data
        #following = data['following']
        #data['user'] = self.context['request'].user
        #follow = Follow.objects.filter(following=following, user=data['user']).exists()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title')
        model = Group
