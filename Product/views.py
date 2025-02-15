from unicodedata import category

from django.shortcuts import render
from django.views.generic import DetailView

from .models import *
# Create your views here.

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/send-otp/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print(request.user)
    # Foydalanuvchining ochiq (tugallanmagan) buyurtmasini olish
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)

    # Agar mahsulot allaqachon savatda bo‘lsa, sonini oshiramiz
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if not created:
        order_item.quantity += 1  # Agar bor bo‘lsa, miqdorini oshiramiz
        order_item.save()

    return redirect("cart")  # Savat sahifasiga qaytarish
@login_required(login_url='/auth/send-otp/')
def cart_view(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()  # Faqat o‘z savatini oladi
    return render(request, "cart.html", {"order": order})
def Index(request):
    product_xit = Product.objects.filter(category=1).all()
    product_sale = Product.objects.filter(category=2).all()
    category = Category.objects.first()
    category2 = Category.objects.last()
    context = {
        'product_xit': product_xit,
        'category': category,
        'category2': category2,

    }
    return render(request,'index.html',context)


@login_required(login_url='/auth/send-otp/')
def increase_quantity(request, item_id):
    """Mahsulot miqdorini oshirish"""
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_completed=False)
    order_item.quantity += 1
    order_item.save()
    return redirect("cart")


@login_required(login_url='/auth/send-otp/')
def decrease_quantity(request, item_id):
    """Mahsulot miqdorini kamaytirish (0 ga yetganda o‘chirish)"""
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_completed=False)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()  # Agar 1 bo‘lsa, butunlay o‘chirib tashlaymiz

    return redirect("cart")

login_required(login_url='/auth/send-otp/')
def DeleteProduct(request, product_id):
    """ Savatdan bitta mahsulot turini butunlay o‘chirish """
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    if order:
        order_item = OrderItem.objects.filter(order=order, product_id=product_id).first()
        if order_item:
            order_item.delete()
    return redirect("cart")  # Savat sahifasiga qaytarish



from unidecode import unidecode

def search_products(request):
    query = request.GET.get('q', '')  # Foydalanuvchi kiritgan so‘z
    category_id = request.GET.get('category', '')

    products = Product.objects.all()

    if query:
        normalized_query = unidecode(query.lower())  # Kirillni lotinga o‘giramiz
        products = products.filter(name__icontains=query) | products.filter(name__icontains=normalized_query)

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()  # Barcha kategoriyalarni olish

    return render(request, 'search_result.html', {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': category_id
    })


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-details.html'
    context_object_name = 'product'