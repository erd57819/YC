from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

# 댓글에 대한 Serializer
class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = Comment
        # 1. 'user' 필드를 fields에 추가합니다.
        fields = ('id', 'user', 'user_nickname', 'content', 'created_at', 'updated_at', 'article')
        # 2. 'user' 필드를 read_only_fields에 추가합니다.
        read_only_fields = ('article', 'user',)

# 게시글 목록에 대한 Serializer
class ArticleListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'user_nickname', 'title', 'content', 'comment_count', 'created_at')

# 게시글 상세 정보에 대한 Serializer
class ArticleSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)
    # comments 필드는 CommentSerializer를 사용하므로, CommentSerializer 수정이 중요합니다.
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        # 3. 'user' 필드를 fields에 추가합니다.
        fields = ('id', 'user', 'user_nickname', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        # 4. 'user' 필드를 read_only_fields에 추가합니다.
        read_only_fields = ('user',)