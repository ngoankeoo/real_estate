from django.urls import path

from django.contrib import admin

# Register your models here.

from .models import Listing
from .views import upload_csv

class ListingAdmin(admin.ModelAdmin):
    change_list_template = "admin/upload_csv.html"
    list_display = ('id', 'title', 'is_published',
                    'price', 'list_data', 'realtor')
    list_display_links = ('id', 'title')
    list_filter = ('realtor',)
    list_editable = ('is_published',)
    search_fields = ('title', 'description', 'address',
                     'city', 'state', 'zipcode', 'price')
    list_per_page = 25

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('upload_csv/', upload_csv),
        ]
        print("My_urls + urls {0}".format(my_urls + urls))
        return my_urls + urls


admin.site.register(Listing, ListingAdmin)
