from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import BoardListSerializer, BoardSerializer, CommentSerializer
from rest_framework.permissions import AllowAny
from .models import Board, Comment

@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def board_list(request, board_type):
    # user = request.user
    
    # if not user.is_authenticated:
    #     return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if request.method == 'GET':
        boards = Board.objects.filter(board_type=board_type)
        if not boards.exists():
            return Response([], status=status.HTTP_200_OK)
        serializer = BoardListSerializer(boards, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data.copy()  # 복사본 생성
        data['board_type'] = board_type  # board_type 추가
        serializer = BoardSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if 'image' in request.FILES:
                serializer.save(image=request.FILES['image'], board_type=board_type)
            else:
                serializer.save(board_type=board_type)  # board_type 명시적 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticated])
def board_detail(request, board_type, board_pk):
    board = get_object_or_404(Board, board_type=board_type, pk=board_pk)
    user = request.user
    
    if not user.is_authenticated:
        return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        serializer = BoardSerializer(board, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BoardSerializer(board, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            if 'image' in request.FILES:
                if board.image:
                    board.image.delete()
                serializer.save(image=request.FILES['image'])
            else:
                if request.data.get('image_clear'):
                    board.image.delete()
                    serializer.save(image=None)
                else:
                    serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if board.image:
            board.image.delete()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def board_like(request, board_type, board_pk):
    try:
        board = get_object_or_404(Board, board_type=board_type, pk=board_pk)
        user = request.user
    
        if not user.is_authenticated:
            return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if board.like_users.filter(pk=user.pk).exists():
            board.like_users.remove(user)
            is_liked = False
        else:
            board.like_users.add(user)
            is_liked = True
        
        return Response({
            'is_liked': is_liked,
            'like_count': board.like_users.count()
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def comment_list(request, board_type, board_pk):
    board = get_object_or_404(Board, board_type=board_type, pk=board_pk)
    user = request.user
    
    if not user.is_authenticated:
        return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        comments = board.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(board=board)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([AllowAny])
def comment_detail(request, board_type, board_pk, comment_pk):
    comment = get_object_or_404(Comment, board__board_type=board_type, pk=comment_pk, board_id=board_pk)
    user = request.user
    
    if not user.is_authenticated:
        return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
@permission_classes([IsAuthenticated])
def comment_like(request, board_type, board_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, board__board_type=board_type, board_id=board_pk)
    user = request.user
    
    if not user.is_authenticated:
        return Response({'detail': '로그인이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if comment.like_users.filter(pk=user.pk).exists():
        comment.like_users.remove(user)
        is_liked = False
    else:
        comment.like_users.add(user)
        is_liked = True
        
    context = {
        'is_liked': is_liked,
        'like_count': comment.like_users.count()
    }
    return Response(context)