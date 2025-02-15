from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('card', 'Karta orqali to‘lov'),
        ('cod', 'Yetkazib berishda to‘lov'),
    ]

    full_name = forms.CharField(label="Ism Familiya", max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label="Telefon raqam", max_length=15,
                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
    payment_method = forms.ChoiceField(label="To‘lov turi", choices=PAYMENT_CHOICES, widget=forms.RadioSelect())
    address = forms.CharField(label="Yetkazib berish manzili", widget=forms.HiddenInput())  # Google Maps dan olinadi
