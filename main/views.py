import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.template.context_processors import request
from django.views.decorators.http import require_safe

from .models import CustomUser,PDFDocument
from .forms import PhoneNumberForm, OTPForm, UserDetailsForm
from django.contrib.auth import login,logout,authenticate

from django.shortcuts import render
from .models import PDFDocument



def send_otp(request):
    if request.method == "POST":
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            is_agreed = form.cleaned_data['is_agreed']

            # 4 xonali kod yaratish
            otp = random.randint(1000, 9999)
            cache.set(phone_number, otp, timeout=300)  # 5 daqiqa saqlanadi

            # SMS API orqali kod yuborish (hozircha faqat terminalga chiqaramiz)
            print(f"Yuborilgan kod: {otp}")

            request.session['phone_number'] = phone_number
            request.session['is_agreed'] = is_agreed  # Rozilikni sessiyada saqlaymiz
            return redirect('verify_otp')

    else:
        form = PhoneNumberForm()
    context = {
        'form': form,
        'pdf': PDFDocument.objects.first(),
    }
    return render(request, 'auth/phone.html', context)




def verify_otp(request):
    phone_number = request.session.get('phone_number')
    is_agreed = request.session.get('is_agreed', False)

    if not phone_number:
        return redirect('send_otp')

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = cache.get(phone_number)

            if stored_otp and str(stored_otp) == otp:
                # ✅ Foydalanuvchini yaratish yoki olish
                user, created = CustomUser.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'is_agree': is_agreed}
                )

                # ✅ Agar oldin yaratilgan bo‘lsa, `is_agree` yangilaymiz
                if not created:
                    user.is_agree = True
                    user.save()

                request.session['user_id'] = user.id  # Sessiyaga saqlash

                # ✅ **Foydalanuvchini avtomatik login qilish**
                login(request, user)  # 🔥 MUHIM!

                return redirect('complete_registration')

            else:
                form.add_error('otp', "Noto‘g‘ri tasdiqlash kodi!")

    else:
        form = OTPForm()

    return render(request, 'auth/verify.html', {'form': form, 'phone_number': phone_number})


@login_required
def complete_registration(request):
    user = request.user  # ✅ Tizimga kirgan foydalanuvchini olamiz

    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = UserDetailsForm(instance=user)

    return render(request, 'auth/complete.html', {'form': form})

def success(request):
    return render(request, 'index.html')


def Product(request):
    return render(request,'about.html')

def Logout(request):
    logout(request)
    return redirect('/auth/send-otp/')

