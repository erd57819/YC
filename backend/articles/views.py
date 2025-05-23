from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from .models import Article, Comment

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 쓰기 가능, 비인증 사용자는 읽기만 가능
def article_list(request):

    if request.method == 'GET':
        articles = Article.objects.all() # 게시글이 없어도 빈 리스트를 반환
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # 게시글 생성은 인증된 사용자만 가능 (IsAuthenticatedOrReadOnly 덕분에)
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user 필드는 현재 로그인한 사용자로 자동 설정
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly]) # 인증된 사용자는 쓰기 가능, 비인증 사용자는 읽기만 가능
def article_detail(request, article_pk):

    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 아래부터는 인증된 사용자만 접근 가능
    elif request.method == 'PUT':
        # 작성자 본인 여부 확인
        if request.user != article.user:
            return Response({'error': 'You are not authorized to edit this article.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ArticleSerializer(instance=article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 작성자 본인 여부 확인
        if request.user != article.user:
            return Response({'error': 'You are not authorized to delete this article.'}, status=status.HTTP_403_FORBIDDEN)
        
        article.delete()
        return Response(data={'message': f'Article {article_pk} has been deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) # 댓글 작성은 인증된 사용자만 가능
def comment_create(request, article_pk):

    article = get_object_or_404(Article, pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # article과 user 필드는 자동으로 채워줌
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated]) # 댓글 수정/삭제는 인증된 사용자만 가능
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user != comment.user:
        return Response({'error': 'You are not authorized to manage this comment.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommentSerializer(instance=comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(data={'message': f'Comment {comment_pk} has been deleted.'}, status=status.HTTP_204_NO_CONTENT)