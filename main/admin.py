from django.contrib import *
from django.contrib import admin

from .models import Price_range,Brand,Color,Ram_and_memory,Product,ProductAttribute,details,Banner,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
# Register your models here.
admin.site.register(Banner)
admin.site.register(Price_range)
class brand(admin.ModelAdmin):
    list_display = ('id','title')
admin.site.register(Brand,brand)

class ColorAdmin(admin.ModelAdmin):
    list_display = ('title','color_bg')
admin.site.register(Color,ColorAdmin)
admin.site.register(Ram_and_memory)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','brand','color','image_tag','Ram_and_memory','status','is_featured')
    list_editable=('status','is_featured',)
admin.site.register(Product,ProductAdmin)

class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=('id','Ram_and_memory','color','image_tag','price')
admin.site.register(ProductAttribute,ProductAttributeAdmin)

class detailsadmin(admin.ModelAdmin):
    list_display = ('title','price','image_tag','is_featured')
    list_editable = ('is_featured',)

class CartOrderAdmin(admin.ModelAdmin):
	list_editable=('paid_status','order_status')
	list_display=('user','total_amt','paid_status','order_dt','order_status')
admin.site.register(CartOrder,CartOrderAdmin)

class CartOrderItemsAdmin(admin.ModelAdmin):
	list_display=('invoice_no','item','image_tag','qty','price','total')
admin.site.register(CartOrderItems,CartOrderItemsAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)

class UserAddressBookAdmin(admin.ModelAdmin):
	list_display=('user','address','status')
admin.site.register(UserAddressBook,UserAddressBookAdmin)

admin.site.register(details,detailsadmin)