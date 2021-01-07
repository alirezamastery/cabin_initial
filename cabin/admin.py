from django.contrib import admin
from .models import *


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'content_type', 'object_id')


@admin.register(Rider)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'x', 'y')


@admin.register(Car)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'car_type', 'model' , 'color')


class CarAdmin(admin.TabularInline):
    model = Car


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name','rating', 'x', 'y', 'active')
    inlines = (CarAdmin,)


@admin.register(RideRequest)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'rider', 'x', 'y', 'car_type')


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('name', 'pickup_time', 'dropoff_time', 'car', 'request',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ride', 'amount', 'status')
