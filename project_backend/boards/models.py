from django.db import models
from django.conf import settings


class Board(models.Model):
    BOARD_CHOICES = (
        ('board1', '일반게시판'),
        ('board2', '챌린지게시판1'),
        ('board3', '챌린지게시판2')
    )
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    # )
    board_type = models.CharField(max_length=20, choices=BOARD_CHOICES, default='board1')
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='board/images/', null=True, blank=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_boards')

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
