import calendar
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Price_range, Brand, details, Product, ProductAttribute, Banner, CartOrder, CartOrderItems, UserAddressBook, ProductReview, Wishlist, UserAddressBook
from .forms import SignupForm,ReviewAdd,AddressBookForm,ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib import messages
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth


def home(request):
    banners = Banner.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured=True).order_by('-id')
    product = Product.objects.all().order_by('-id')
    return render(request, "main/index.html", {'data': data, 'banners': banners, 'product': product})


def category_list(request):
    data = Price_range.objects.all().order_by('-id')
    return render(request, 'main/category_list.html', {'data': data})


def brand_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request, "main/brand_list.html", {'data': data})


def Apple(request):
    data = details.objects.all().order_by('-id')
    return render(request, "main/brand_list.html", {'data': data})


def product_list(request):
    data = Product.objects.all().order_by('-id')
    cats = Product.objects.distinct().values(
        'Price_range__title', 'Price_range__id')
    brands = Product.objects.distinct().values('brand__title', 'brand__id')
    colors = ProductAttribute.objects.distinct().values(
        'color__title', 'color__id', 'color__color_code')
    Ram_and_memory = ProductAttribute.objects.distinct().values(
        'Ram_and_memory__title', 'Ram_and_memory__id')
    return render(request, "main/product_list.html",
                  {
                      'data': data,
                      'cats': cats,
                      'brands': brands,
                      'colors': colors,
                      'sizes': Ram_and_memory,

                  }
                  )

# product list according


def category_product_list(request, cat_id):
    category = Price_range.objects.get(id=cat_id)
    data = Product.objects.filter(Price_range=category).order_by('-id')
    cats = Product.objects.distinct().values(
        'Price_range__title', 'Price_range__id')
    brands = Product.objects.distinct().values('brand__title', 'brand__id')
    colors = ProductAttribute.objects.distinct().values(
        'color__title', 'color__id', 'color__color_code')
    Ram_and_memory = ProductAttribute.objects.distinct().values(
        'Ram_and_memory__title', 'Ram_and_memory__id')
    return render(request, "main/category_product_list.html", {'data': data, 'cats': cats,
                                                               'brands': brands,
                                                               'colors': colors,
                                                               'sizes': Ram_and_memory, })


def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    cats = Product.objects.distinct().values(
        'Price_range__title', 'Price_range__id')
    brands = Product.objects.distinct().values('brand__title', 'brand__id')
    colors = ProductAttribute.objects.distinct().values(
        'color__title', 'color__id', 'color__color_code')
    Ram_and_memory = ProductAttribute.objects.distinct().values(
        'Ram_and_memory__title', 'Ram_and_memory__id')
    return render(request, "main/category_product_list.html", {'data': data, 'cats': cats,
                                                               'brands': brands,
                                                               'colors': colors,
                                                               'sizes': Ram_and_memory, })


def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    colors = ProductAttribute.objects.filter(product=product).values(
        'color__id', 'color__title', 'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values(
        'Ram_and_memory__id', 'Ram_and_memory__title', 'price', 'color__id').distinct()
    related_products = Product.objects.filter(
        Price_range=product.Price_range).exclude(id=id)[:4]
    reviewForm = ReviewAdd()

     # Check
    canAdd = True
    reviewCheck = ProductReview.objects.filter(user=request.user, product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
    # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'main/product_detail.html', {'data': product, 'related': related_products, 'colors':colors,'sizes':sizes,'reviewForm':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})


def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    print(request.GET)
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


def cart(request):
    total_amt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():

            total_amt += (int(item['qty'])*float(item['price']))//81
        return render(request, 'main/cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt})
    else:
        return render(request, 'main/cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})

# Delete Cart Item


def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('main/ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})

# update cart item


def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
    t = render_to_string('main/ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
        if form.is_valid() == False:
            messages.info(
                request, 'The Password or Username you entered is not valid')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def checkout(request):
    total_amt = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty'])*float(item['price'])
        # Order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt
        )
        # End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
            # OrderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
            )
            # End
        # Process Payment
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-'+str(order.id),
            'invoice': 'INV-'+str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = UserAddressBook.objects.filter(
            user=request.user, status=True).first()
        return render(request, 'main/checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt':total_amt,'form':form,'address':address})


@csrf_exempt
def payment_done(request):
    returnData = request.POST
    return render(request, 'main/payment-success.html', {'data': returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'main/payment-fail.html')

# Search


def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'main/search.html', {'data': data})


def filter_data(request):
    colors = request.GET.getlist('color[]')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(colors) > 0:
        allProducts = allProducts.filter(
            productattribute__color__id__in=colors).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(
            Price_range__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            productattribute__Ram_and_memory__id__in=sizes).distinct()
    t = render_to_string('main/ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})

# Wishlist
def add_wishlist(request):
	pid=request.GET['product']
	product=Product.objects.get(pk=pid)
	data={}
	checkw=Wishlist.objects.filter(product=product,user=request.user).count()
	if checkw > 0:
		data={
			'bool':False
		}
	else:
		wishlist=Wishlist.objects.create(
			product=product,
			user=request.user
		)
		data={
			'bool':True
		}
	return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
	wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
	return render(request, 'user/wishlist.html',{'wlist':wlist})

# My Reviews


def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews': reviews})

# My AddressBook


def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html', {'addbook': addbook})
# Save Review


def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.POST['review_text'],
        review_rating=request.POST['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.POST['review_text'],
        'review_rating': request.POST['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


# User Dashboard


def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})

# My Orders


def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})

# Order Detail


def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})

# Save addressbook
def save_address(request):
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm
	return render(request, 'user/add-address.html',{'form':form,'msg':msg})

# Activate address
def activate_address(request):
	a_id=str(request.GET['id'])
	UserAddressBook.objects.update(status=False)
	UserAddressBook.objects.filter(id=a_id).update(status=True)
	return JsonResponse({'bool':True})

# Edit Profile
def edit_profile(request):
	msg=None
	if request.method=='POST':
		form=ProfileForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			msg='Data has been saved'
	form=ProfileForm(instance=request.user)
	return render(request, 'user/edit-profile.html',{'form':form,'msg':msg})

# Update addressbook
def update_address(request,id):
	address=UserAddressBook.objects.get(pk=id)
	msg=None
	if request.method=='POST':
		form=AddressBookForm(request.POST,instance=address)
		if form.is_valid():
			saveForm=form.save(commit=False)
			saveForm.user=request.user
			if 'status' in request.POST:
				UserAddressBook.objects.update(status=False)
			saveForm.save()
			msg='Data has been saved'
	form=AddressBookForm(instance=address)
	return render(request, 'user/update-address.html',{'form':form,'msg':msg})