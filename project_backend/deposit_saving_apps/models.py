from django.db import models
from django.conf import settings
# Create your models here.

# 예금


class DepositProducts(models.Model):
    user_contains = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='deposit_contains')
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융 회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField()  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField()  # 우대 조건
    mtrt_int = models.TextField()  # 만기 후 이자율
    join_way_smart = models.IntegerField(default=0)  # 가입방법 스마트폰
    join_way_internet = models.IntegerField(default=0)  # 가입방법 인터넷
    join_way_store = models.IntegerField(default=0)  # 가입방법 직영점
    Deposit_code = models.IntegerField(default=1)
    # max_limit = models.TextField() # 최고 한도

    
class DepositOptions(models.Model):
    deposit_product = models.ForeignKey(
        DepositProducts, on_delete=models.CASCADE)  # 적금 상품 ID
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    intr_rate = models.FloatField()  # 저축 금리
    intr_rate2 = models.FloatField()  # 저축 우대 금리
    save_trm = models.IntegerField()  # 저축 기간
    # rsrv_type = models.TextField()  # 적립 유형
    # rsrv_type_nm = models.TextField()  # 적립 유형명

# 적금


class SavingProducts(models.Model):
    user_contains = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='saving_contains')
    fin_prdt_cd = models.TextField(unique=True)  # 금융상품 코드
    kor_co_nm = models.TextField()  # 금융 회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    etc_note = models.TextField()  # 기타 유의사항
    join_deny = models.IntegerField()  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    join_way = models.TextField()  # 가입 방법
    spcl_cnd = models.TextField()  # 우대 조건
    mtrt_int = models.TextField()  # 만기 후 이자율
    join_way_smart = models.IntegerField(default=0)  # 가입방법 스마트폰
    join_way_internet = models.IntegerField(default=0)  # 가입방법 인터넷
    join_way_store = models.IntegerField(default=0)  # 가입방법 직영점
    Saving_code = models.IntegerField(default=2)
    # max_limit = models.TextField() # 최고 한도


class SavingOptions(models.Model):
    saving_product = models.ForeignKey(
        SavingProducts, on_delete=models.CASCADE)  # 적금 상품 ID
    fin_prdt_cd = models.TextField()  # 금융상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축 금리 유형명
    intr_rate = models.FloatField()  # 저축 금리
    intr_rate2 = models.FloatField()  # 저축 우대 금리
    save_trm = models.IntegerField()  # 저축 기간
    rsrv_type = models.TextField()  # 적립 유형
    rsrv_type_nm = models.TextField()  # 적립 유형명
