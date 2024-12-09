from django.db import models

# Create your models here.

class Exchange(models.Model):
    cur_unit = models.TextField() # 통화모델
    ttb = models.TextField() # 송금 받을 때
    tts = models.TextField() # 송금 보낼 때
    cur_nm = models.TextField() # 국가 통화명
    deal_bas_r = models.TextField() # 매매 기준률
    # BKPR = models.TextField() #장부가격