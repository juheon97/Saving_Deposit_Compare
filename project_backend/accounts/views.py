from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from deposit_saving_apps.models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
import random
import string


@api_view(['GET', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):

    if request.method == "GET":
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "gender": user.gender,
            "age": user.age,
            "first_name": user.first_name,
            "image": request.build_absolute_uri(user.image.url) if user.image else None,
            "balance_deposit": user.balance_deposit,
            "balance_saving": user.balance_saving
            # "image": user.image.url if user.image else None,
            # "balance": user.balance,
            # "target_amount": user.target_amount,
            # "target_date": user.target_date,
        }
        return Response(user_data)
    elif request.method == "PATCH":
        user = request.user
        data = request.data

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'email' in data:
            user.email = data['email']
        if 'gender' in data:
            user.gender = data['gender']
        if 'age' in data:
            user.age = data['age']
        if 'balance_deposit' in data:
            user.balance_deposit = data['balance_deposit']
        if 'balance_saving' in data:
            user.balance_saving = data['balance_saving']

        try:
            user.full_clean()
            user.save()
            return Response({
                "message": "Successfully updated",
                "user": {
                    "first_name": user.first_name,
                    "email": user.email,
                    "gender": user.gender,
                    "age": user.age,
                    "balance_deposit": user.balance_deposit,
                    "balance_saving": user.balance_saving
                }
            })
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    if request.FILES.get('image'):
        user = request.user
        user.image = request.FILES['image']
        user.save()
        return Response({
            'message': 'Image updated successfully',
            'image': request.build_absolute_uri(user.image.url)
        })
    return Response({'error': 'No image provided'}, status=400)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_products(request):
    user = request.user

    # 예금 상품 가져오기
    deposit_products = DepositProducts.objects.filter(
        user_contains=user).prefetch_related('depositoptions_set')
    deposit_data = []
    for product in deposit_products:
        options = product.depositoptions_set.all().order_by('-save_trm')
        deposit_data.append({
            'id': product.id,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'Deposit_code': product.Deposit_code,
            'join_member': product.join_member,
            'join_way': product.join_way,
            'spcl_cnd': product.spcl_cnd,
            'mtrt_int': product.mtrt_int,
            'etc_note': product.etc_note,
            'options': [
                {
                    'save_trm': option.save_trm,
                    'intr_rate': option.intr_rate,
                    'intr_rate2': option.intr_rate2,
                }
                for option in options
            ]
        })

    # 적금 상품 가져오기
    saving_products = SavingProducts.objects.filter(
        user_contains=user).prefetch_related('savingoptions_set')
    saving_data = []
    for product in saving_products:
        options = product.savingoptions_set.all().order_by('-save_trm')
        saving_data.append({
            'id': product.id,
            'kor_co_nm': product.kor_co_nm,
            'fin_prdt_nm': product.fin_prdt_nm,
            'Saving_code': product.Saving_code,
            'join_member': product.join_member,
            'join_way': product.join_way,
            'spcl_cnd': product.spcl_cnd,
            'mtrt_int': product.mtrt_int,
            'etc_note': product.etc_note,
            'options': [
                {
                    'save_trm': option.save_trm,
                    'intr_rate': option.intr_rate,
                    'intr_rate2': option.intr_rate2,
                }
                for option in options
            ]
        })

    # 두 리스트 합치기
    all_products = deposit_data + saving_data

    return Response(all_products)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user_product(request, type, product_id):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=401)

        if type == 'deposit':
            product = DepositProducts.objects.get(id=product_id)
            product.user_contains.remove(user)
        elif type == 'saving':
            product = SavingProducts.objects.get(id=product_id)
            product.user_contains.remove(user)

        return Response({"message": "Successfully deleted"})
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password1 = request.data.get('new_password1')
    new_password2 = request.data.get('new_password2')

    # 기본 유효성 검사
    if not all([old_password, new_password1, new_password2]):
        return Response(
            {'message': '모든 필드를 입력해주세요.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 현재 비밀번호 확인
    if not user.check_password(old_password):
        return Response(
            {'message': '현재 비밀번호가 일치하지 않습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 새 비밀번호 일치 확인
    if new_password1 != new_password2:
        return Response(
            {'message': '새 비밀번호가 일치하지 않습니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 새 비밀번호 유효성 검사
    if len(new_password1) < 8:
        return Response(
            {'message': '비밀번호는 최소 8자 이상이어야 합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 현재 비밀번호와 새 비밀번호가 같은지 확인
    if old_password == new_password1:
        return Response(
            {'message': '새 비밀번호는 현재 비밀번호와 달라야 합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # 비밀번호 변경
        user.set_password(new_password1)
        user.save()

        # 세션 유지를 위한 처리
        update_session_auth_hash(request, user)

        return Response(
            {'message': '비밀번호가 성공적으로 변경되었습니다.'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'message': '비밀번호 변경 중 오류가 발생했습니다.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


User = get_user_model()
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    username = request.data.get('username')
    email = request.data.get('email')

    try:
        user = User.objects.get(username=username, email=email)

        # 임시 비밀번호 생성 (6글자 + 특수문자 2개)
        letters = string.ascii_letters
        symbols = '!@#$%^&*'
        temp_password = ''.join(random.choice(letters) for i in range(6)) + \
            ''.join(random.choice(symbols) for i in range(2))

        # 비밀번호 섞기
        temp_password = ''.join(random.sample(
            temp_password, len(temp_password)))

        # 사용자 비밀번호 업데이트
        user.password = make_password(temp_password)
        user.save()

        return Response({
            'success': True,
            'temp_password': temp_password,
            'message': '임시 비밀번호가 생성되었습니다.'
        })
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': '일치하는 사용자 정보를 찾을 수 없습니다.'
        }, status=404)
