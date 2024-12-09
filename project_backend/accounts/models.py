from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [('M', '남성'), ('F', '여성'),]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    balance_saving = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    balance_deposit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # target_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # target_date = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(blank=False,null=False)
    image = models.ImageField(blank=True, upload_to='user_images/', default='default.png')   
    REQUIRED_FIELDS = ['email', 'first_name', 'gender', 'age']