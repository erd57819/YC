from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_nickname', 'content', 'created_at', 'updated_at', 'article')
        read_only_fields = ('article', 'user',)

class ArticleListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'user_nickname', 'title', 'content', 'comment_count', 'created_at')

class ArticleSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'user', 'user_nickname', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        read_only_fields = ('user',)