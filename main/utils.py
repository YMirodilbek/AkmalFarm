import random
import datetime
from .models import OTPCode

def generate_otp(phone_number):
    """ Yangi OTP yaratib, eski kodlarni o‘chiradi """
    OTPCode.objects.filter(phone_number=phone_number).delete()  # Eski kodlarni o‘chirish
    code = random.randint(1000, 9999)  # 4 xonali tasdiqlash kodi
    OTPCode.objects.create(phone_number=phone_number, code=code, created_at=datetime.datetime.now())
    print(f"📩 Yangi tasdiqlash kodi: {code}")  # SMS API o‘rniga konsolga chiqaramiz
    return code
