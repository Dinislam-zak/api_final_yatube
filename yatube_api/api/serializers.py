from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Post, Comment, Follow, Group

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'text', 'pub_date', 'image', 'group']
        read_only_fields = ['id', 'author', 'pub_date']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created', 'post']
        read_only_fields = ['id', 'author', 'created', 'post']


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны на этого пользователя.'
            )
        ]

    def validate(self, data):
        if data['following'] == self.context['request'].user:
            raise serializers.ValidationError('Нельзя подписаться на себя.')
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']
