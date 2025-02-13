import random
from django.shortcuts import render, redirect
from django.core.cache import cache
from .models import CustomUser,PDFDocument
from .forms import PhoneNumberForm, OTPForm, UserDetailsForm

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
    phone_number = request.session.get('phone_number')  # ✅ Sessiyadan olamiz
    is_agreed = request.session.get('is_agreed', False)  # ✅ Default False

    if not phone_number:
        return redirect('send_otp')

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            stored_otp = cache.get(phone_number)

            if stored_otp and str(stored_otp) == otp:
                # ✅ Foydalanuvchi mavjud yoki yaratiladi
                user, created = CustomUser.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'is_agree': is_agreed}
                )

                if not created:  # ✅ Foydalanuvchi oldin mavjud bo‘lsa
                    return redirect('success')

                # ✅ `is_agree` yangilanayotganini tekshiramiz
                user.is_agree = True
                user.save()

                request.session['user_id'] = user.id
                return redirect('complete_registration')

            else:
                form.add_error('otp', "Noto‘g‘ri tasdiqlash kodi!")

    else:
        form = OTPForm()

    return render(request, 'auth/verify.html', {'form': form, 'phone_number': phone_number})

def complete_registration(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('send_otp')

    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        form = UserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('success')

    else:
        form = UserDetailsForm(instance=user)

    return render(request, 'auth/complete.html', {'form': form})


def success(request):
    return render(request, 'success.html')
