from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'board', 'created_at', 'updated_at', 
                 'like_count', 'is_liked', 'like_users')
        read_only_fields = ('board', 'like_users')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.like_users.filter(pk=request.user.pk).exists()

class BoardListSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'title', 'content', 'image', 'board_type', 'created_at', 'updated_at', 'like_count', 'is_liked')

    def get_like_count(self, obj):
        return obj.like_users.count()
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.like_users.filter(pk=request.user.pk).exists()
class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'title', 'content', 'created_at', 'updated_at','image', 
                 'comments', 'like_count', 'is_liked', 'like_users', 'board_type') # board_type 추가
        read_only_fields = ('like_users',)
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.like_users.filter(pk=request.user.pk).exists()