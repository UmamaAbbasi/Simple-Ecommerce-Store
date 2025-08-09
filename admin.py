from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import Product, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_paid']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


class CustomAdminSite(admin.AdminSite):
    site_header = 'E-Shop Admin'
    site_title = 'E-Shop Admin Portal'
    index_title = 'Welcome to E-Shop Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        paid_orders = Order.objects.filter(is_paid=True)
        total_revenue = sum(order.get_total() for order in paid_orders)

        context = {
            **self.each_context(request),
            'orders': Order.objects.count(),
            'users': User.objects.count(),
            'revenue': total_revenue,
        }
        return render(request, 'admin/dashboard.html', context)


# Instantiate custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models
custom_admin_site.register


