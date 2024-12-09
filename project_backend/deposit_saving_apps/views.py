from logging import raiseExceptions
from multiprocessing import JoinableQueue
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from django.conf import settings
from .serializers import DepositProductsSerializer, DepositOptionsSerializer, SavingProductsSerializer, SavingOptionsSerializer
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import time


# Create your views here.


BASE_URL = "http://finlife.fss.or.kr/finlifeapi/"


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def save_deposit_products(request):
    URL = BASE_URL + "depositProductsSearch.json"
    page = 1
    total_count = 0
    products_saved = 0
    options_saved = 0

    while True:
        params = {
            'auth': settings.APP_KEY,
            'topFinGrpNo': '020000',
            'pageNo': page
        }

        try:
            response = requests.get(URL, params=params).json()
            result = response.get('result', {})

            if page == 1:
                total_count = result.get('total_count', 0)
                if total_count == 0:
                    return JsonResponse({'message': 'No data available'}, status=404)

            if not result.get('baseList'):
                break

            for li in result.get('baseList', []):
                fin_prdt_cd = li.get('fin_prdt_cd', '-1')
                kor_co_nm = li.get('kor_co_nm', '-1')
                fin_prdt_nm = li.get('fin_prdt_nm', '-1')
                etc_note = li.get('etc_note', '-1')
                join_deny = 1 if li.get('join_deny') else -1
                join_member = li.get('join_member', '-1')
                join_way = li.get('join_way', '-1')
                spcl_cnd = li.get('spcl_cnd', '-1')
                mtrt_int = li.get('mtrt_int', '-1')

                # Parse join_way string to determine method availability
                join_way_str = join_way.lower() if join_way != '-1' else ''
                join_way_smart = 1 if '스마트폰' in join_way_str else 0
                join_way_internet = 1 if '인터넷' in join_way_str else 0
                join_way_store = 1 if '영업점' in join_way_str else 0

                product_instance, created = DepositProducts.objects.update_or_create(
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        'kor_co_nm': kor_co_nm,
                        'fin_prdt_nm': fin_prdt_nm,
                        'etc_note': etc_note,
                        'join_deny': join_deny,
                        'join_member': join_member,
                        'join_way': join_way,
                        'spcl_cnd': spcl_cnd,
                        'mtrt_int': mtrt_int,
                        'join_way_smart': join_way_smart,
                        'join_way_internet': join_way_internet,
                        'join_way_store': join_way_store,
                    }
                )
                products_saved += 1

            for li in result.get('optionList', []):
                fin_prdt_cd = li.get('fin_prdt_cd', '-1')
                intr_rate_type_nm = li.get('intr_rate_type_nm', '-1')
                intr_rate = li.get('intr_rate', -1)
                intr_rate2 = li.get('intr_rate2', -1)
                save_trm = li.get('save_trm', -1)

                if fin_prdt_cd and fin_prdt_cd != '-1':
                    product = DepositProducts.objects.filter(
                        fin_prdt_cd=fin_prdt_cd).first()

                    if product:
                        option_instance, created = DepositOptions.objects.update_or_create(
                            deposit_product=product,
                            intr_rate_type_nm=intr_rate_type_nm,
                            save_trm=save_trm if save_trm is not None else -1,
                            defaults={
                                'fin_prdt_cd': fin_prdt_cd,
                                'intr_rate': intr_rate if intr_rate is not None else -1,
                                'intr_rate2': intr_rate2 if intr_rate2 is not None else -1,
                            }
                        )
                        options_saved += 1

            page += 1
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'message': f'API request failed: {str(e)}',
                'products_saved': products_saved,
                'options_saved': options_saved,
                'pages_processed': page - 1
            }, status=500)

        except Exception as e:
            return JsonResponse({
                'message': f'An error occurred: {str(e)}',
                'products_saved': products_saved,
                'options_saved': options_saved,
                'pages_processed': page - 1
            }, status=500)

    return JsonResponse({
        'message': 'Data saved successfully',
        'total_count': total_count,
        'products_saved': products_saved,
        'options_saved': options_saved,
        'pages_processed': page - 1
    }, status=201)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def save_saving_products(request):
    URL = BASE_URL + "savingProductsSearch.json"
    page = 1
    total_count = 0
    products_saved = 0
    options_saved = 0

    while True:
        params = {
            'auth': settings.APP_KEY,
            'topFinGrpNo': '020000',
            'pageNo': page
        }

        try:
            response = requests.get(URL, params=params).json()
            result = response.get('result', {})

            if page == 1:
                total_count = result.get('total_count', 0)
                if total_count == 0:
                    return JsonResponse({'message': 'No data available'}, status=404)

            if not result.get('baseList'):
                break

            for li in result.get('baseList', []):
                fin_prdt_cd = li.get('fin_prdt_cd', '-1')
                kor_co_nm = li.get('kor_co_nm', '-1')
                fin_prdt_nm = li.get('fin_prdt_nm', '-1')
                etc_note = li.get('etc_note', '-1')
                join_deny = 1 if li.get('join_deny') else -1
                join_member = li.get('join_member', '-1')
                join_way = li.get('join_way', '-1')
                spcl_cnd = li.get('spcl_cnd', '-1')
                mtrt_int = li.get('mtrt_int', '-1')

                # Parse join_way string for methods
                join_way_str = join_way.lower() if join_way != '-1' else ''
                join_way_smart = 1 if '스마트폰' in join_way_str else 0
                join_way_internet = 1 if '인터넷' in join_way_str else 0
                join_way_store = 1 if '영업점' in join_way_str else 0

                product_instance, created = SavingProducts.objects.update_or_create(
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        'kor_co_nm': kor_co_nm,
                        'fin_prdt_nm': fin_prdt_nm,
                        'etc_note': etc_note,
                        'join_deny': join_deny,
                        'join_member': join_member,
                        'join_way': join_way,
                        'spcl_cnd': spcl_cnd,
                        'mtrt_int': mtrt_int,
                        'join_way_smart': join_way_smart,
                        'join_way_internet': join_way_internet,
                        'join_way_store': join_way_store,
                    }
                )
                products_saved += 1

            for li in result.get('optionList', []):
                fin_prdt_cd = li.get('fin_prdt_cd', '-1')
                intr_rate_type_nm = li.get('intr_rate_type_nm', '-1')
                intr_rate = li.get('intr_rate', -1)
                intr_rate2 = li.get('intr_rate2', -1)
                save_trm = li.get('save_trm', -1)
                rsrv_type = li.get('rsrv_type', '-1')
                rsrv_type_nm = li.get('rsrv_type_nm', '-1')

                if fin_prdt_cd and fin_prdt_cd != '-1':
                    product = SavingProducts.objects.filter(
                        fin_prdt_cd=fin_prdt_cd).first()

                    if product:
                        option_instance, created = SavingOptions.objects.update_or_create(
                            saving_product=product,
                            intr_rate_type_nm=intr_rate_type_nm,
                            save_trm=save_trm if save_trm is not None else -1,
                            defaults={
                                'fin_prdt_cd': fin_prdt_cd,
                                'intr_rate': intr_rate if intr_rate is not None else -1,
                                'intr_rate2': intr_rate2 if intr_rate2 is not None else -1,
                                'rsrv_type': rsrv_type,
                                'rsrv_type_nm': rsrv_type_nm,
                            }
                        )
                        options_saved += 1

            page += 1
            time.sleep(2)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'message': f'API request failed: {str(e)}',
                'products_saved': products_saved,
                'options_saved': options_saved,
                'pages_processed': page - 1
            }, status=500)

        except Exception as e:
            return JsonResponse({
                'message': f'An error occurred: {str(e)}',
                'products_saved': products_saved,
                'options_saved': options_saved,
                'pages_processed': page - 1
            }, status=500)

    return JsonResponse({
        'message': 'Data saved successfully',
        'total_count': total_count,
        'products_saved': products_saved,
        'options_saved': options_saved,
        'pages_processed': page - 1
    }, status=201)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_deposit_products(request):
    if request.method == 'GET':
        exchanges = DepositProducts.objects.all()
        serializers = DepositProductsSerializer(exchanges, many=True)
        return Response(serializers.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_deposit_options(request):
    if request.method == 'GET':
        exchanges = DepositOptions.objects.all()
        serializers = DepositOptionsSerializer(exchanges, many=True)
        return Response(serializers.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_saving_products(request):
    if request.method == 'GET':
        exchanges = SavingProducts.objects.all()
        serializers = SavingProductsSerializer(exchanges, many=True)
        return Response(serializers.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_saving_options(request):
    if request.method == 'GET':
        exchanges = SavingOptions.objects.all()
        serializers = SavingOptionsSerializer(exchanges, many=True)
        return Response(serializers.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def toggle_container(request):
    if not request.user.is_authenticated:
        return Response({'error': '로그인이 필요합니다.'}, status=401)

    product_id = request.data.get('product_id')
    product_type = request.data.get('product_type')

    try:
        if product_type == 'deposit':
            product = DepositProducts.objects.get(id=product_id)
            if request.user in product.user_contains.all():
                product.user_contains.remove(request.user)
                return Response({'message': '상품이 제거되었습니다.', 'is_contained': False})
            else:
                product.user_contains.add(request.user)
                return Response({'message': '상품이 담겼습니다.', 'is_contained': True})

        elif product_type == 'saving':
            product = SavingProducts.objects.get(id=product_id)
            if request.user in product.user_contains.all():
                product.user_contains.remove(request.user)
                return Response({'message': '상품이 제거되었습니다.', 'is_contained': False})
            else:
                product.user_contains.add(request.user)
                return Response({'message': '상품이 담겼습니다.', 'is_contained': True})

    except (DepositProducts.DoesNotExist, SavingProducts.DoesNotExist):
        return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contained_products(request):
    user = request.user
    
    # 예금 상품 조회
    deposit_products = DepositProducts.objects.filter(user_contains=user)
    deposit_ids = [{'id': product.id, 'type': 'deposit'} for product in deposit_products]
    
    # 적금 상품 조회
    saving_products = SavingProducts.objects.filter(user_contains=user)
    saving_ids = [{'id': product.id, 'type': 'saving'} for product in saving_products]
    
    # 모든 담은 상품의 ID와 타입을 합쳐서 반환
    contained_products = deposit_ids + saving_ids
    
    return Response({
        'products': contained_products
    })
