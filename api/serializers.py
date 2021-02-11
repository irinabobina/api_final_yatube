from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    post = serializers.SlugRelatedField(read_only=True,
                                        slug_field='id')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Подписчик и автор совпадают')
        return data

    class Meta:
        fields = '__all__'
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        #  Оставляю, как есть, иначе автотесты не пропускают.
        #  Плюс такой набор полей предусмотрен в ТЗ.
        fields = ('title', 'id',)
        model = Group

