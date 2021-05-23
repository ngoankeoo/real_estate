from django.shortcuts import render
from django.http import HttpResponse
from listings.models import Listing
from realtors.models import Realtor
from listings.choices import price_choices, bedroom_choices


# Create your views here.
def index(request):
    listings = Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    district = Listing.objects.order_by('district').distinct().values_list('district', flat=True)
    print('index list district', list(district))
    context = {
        'listings': listings,
        'district_choices': list(district),
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
    }
    return render(request, 'pages/index.html', context)


def about(request):
    realtors = Realtor.objects.order_by('-hire_date')

    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)
