from django.contrib import admin
from bikeapp.models import Bike
# Register your models here.
class BikeAdmin(admin.ModelAdmin):
    list_display=['id','brand','name','type','price','year']
    list_filter=['brand','type','price','year']
admin.site.register(Bike,BikeAdmin)