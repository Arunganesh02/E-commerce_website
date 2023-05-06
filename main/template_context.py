from .models import Product,ProductAttribute
from django.db.models import Min,Max
def get_filters(request):
	cats=Product.objects.distinct().values('Price_range__title','Price_range__id')
	brands=Product.objects.distinct().values('brand__title','brand__id')
	colors=ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
	sizes=ProductAttribute.objects.distinct().values('Ram_and_memory__title','Ram_and_memory__id')
	minMaxPrice=ProductAttribute.objects.aggregate(Min('price'),Max('price'))
	data={
		'cats':cats,
		'brands':brands,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
	}
	return data