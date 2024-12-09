from logging import raiseExceptions
from multiprocessing import JoinableQueue
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import requests
from django.http import JsonResponse
from django.conf import settings
from .serializers import ExchangeSerializer
from .models import Exchange
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import AllowAny
import time

# Create your views here.

BASE_URL="https://www.koreaexim.go.kr/site/program/financial/exchangeJSON"

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_exchange(request):
    params = {
        'authkey': settings.EXCHANGE_KEY,
        'data': 'AP01'
    }
    try:
        response = requests.get(BASE_URL, params=params, verify=False, timeout=10).json()
        
        # 응답이 리스트이므로 바로 순회
        for item in response:
            cur_unit = item.get('cur_unit')
            ttb = item.get('ttb')
            tts = item.get('tts')
            cur_nm = item.get('cur_nm')
            deal_bas_r = item.get('deal_bas_r')
            # BKPR = item.get('BKPR')


            exchange_instance, created = Exchange.objects.update_or_create(
                cur_unit = cur_unit,
                defaults={
                    'ttb': ttb,
                    'tts': tts,
                    'cur_nm': cur_nm,
                    'deal_bas_r': deal_bas_r,
                    # 'BKPR': BKPR
                }
            )
        return JsonResponse({'message': 'Data Saved successfully'}, status=201)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def get_exchange_info(request):
    if request.method == 'GET':
        exchanges = Exchange.objects.all()
        serializers = ExchangeSerializer(exchanges, many=True)
        return Response(serializers.data)