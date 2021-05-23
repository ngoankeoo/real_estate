from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from django.forms import forms
from django.shortcuts import redirect
from realtors.models import Realtor
from listings.models import Listing
import pandas


# Create your views here.
class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


def index(request):
    listings = Listing.objects.order_by('-list_data').filter(is_published=True)

    paginator = Paginator(listings, 20)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }
    return render(request, 'listings/listings.html', context)


def lisitng(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_data')
    districts = Listing.objects.order_by('district').distinct().values_list('district', flat=True)
    # keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'district' in request.GET:
        district = request.GET['district']
        if district:
            queryset_list = queryset_list.filter(district=district)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'district_choices': list(districts),
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }

    return render(request, 'listings/search.html', context)


def upload_csv(request):
    """

    :param request:
    :return:
    """

    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        df = pandas.read_csv(csv_file)
        # print(df)
        count = 0
        for row in df.iterrows():
            # print(row)
            data = row[1]
            price = data['price']
            location = data['location']
            title = data['title']
            image = data['image']
            content = data['content']
            area = data['area']
            up_time = data['up_time']
            contact_name = data['contact_name']
            contact_phone = data['contact_phone']
            realtor = Realtor(name=contact_name, phone=contact_phone, description="This is realtor from crawler")
            district = location.split(',')[0].strip()
            state = location.split(',')[1].strip()
            if area == "Không xác định":
                area = 0
            else:
                area = area.split()[0]

            if price != "Giá thỏa thuận":
                print(price)
                price_split = price.split()
                if area == 0:
                    price = 0
                elif price_split[1] == "tỷ":
                    price = round(float(price_split[0]) * 1000 / float(area), 2)
                elif price_split[1] == "triệu":
                    price = round(float(price_split[0]) / float(area), 2)
                else:
                    price = round(float(price_split[0]), 2)
            else:
                price = 0
            print('price:  {0} trieu/m2'.format(price))
            print('sqrt: {0} m2'.format(area))
            realtor.save()
            listing = Listing(realtor=realtor, address=location,district=district,
                              image_link=image, title=title, price=price,
                              description=content, sqft=area, state=state,
                              city=location.split(',')[1])
            listing.save()

        return redirect("..")
    form = CsvImportForm()
    payload = {"form": form}
    return render(
        request, "admin/csv_form.html", payload
    )
