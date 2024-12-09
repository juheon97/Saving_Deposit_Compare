from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from allauth.account.adapter import get_adapter
from .models import User

class UserDetailSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'gender', 'age', 'image', 'balance_deposit', 'balance_saving')
        read_only_fields = ('image', 'balance_deposit', 'balance_saving')

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
    age = serializers.IntegerField(required=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'first_name': self.validated_data.get('first_name', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age'),

        })
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        
        # 필수 필드들을 먼저 설정
        user.first_name = self.cleaned_data.get('first_name')
        user.gender = self.cleaned_data.get('gender')
        user.age = self.cleaned_data.get('age')
        user.image = 'default.png'
        
        adapter.save_user(request, user, self)
        
        return user

# from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from dj_rest_auth.serializers import UserDetailsSerializer
# from django.contrib.auth.password_validation import validate_password
# from .models import User

# class UserDetailSerializer(UserDetailsSerializer):
#     class Meta(UserDetailsSerializer.Meta):
#         model = User
#         fields = ('id', 'username', 'email', 'first_name', 'gender', 'age',
#                  'balance', 'target_amount', 'target_date')
#         read_only_fields = ('balance', 'target_amount', 'target_date')

# class CustomRegisterSerializer(RegisterSerializer):
#     first_name = serializers.CharField(required=True)
#     gender = serializers.ChoiceField(choices=User.GENDER_CHOICES, required=True)
#     age = serializers.IntegerField(required=True)
    
#     def validate_password1(self, password):
#         validate_password(password)
#         return password

#     def save(self, request):
#         user = User(
#             username=self.validated_data.get('username'),
#             email=self.validated_data.get('email', ''),
#             first_name=self.validated_data.get('first_name'),
#             gender=self.validated_data.get('gender'),
#             age=self.validated_data.get('age')
#         )
        
#         user.set_password(self.validated_data.get('password1'))
#         user.save()
        
#         return user