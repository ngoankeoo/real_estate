from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, sqrt_choices, state_choices
from django.forms import forms
from django.shortcuts import redirect
from realtors.models import Realtor
from listings.models import Listing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
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
    relate_listing = []
    print(listing.relate_real_estate.split(','))
    for id in listing.relate_real_estate.split(','):
        if id != '':
            relate_listing.append(get_object_or_404(Listing, pk=int(id)))
    context = {
        'listing': listing,
        'relate_listing': relate_listing,
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
    if 'sqrt' in request.GET:
        sqrt = request.GET['sqrt']
        if sqrt:
            queryset_list = queryset_list.filter(sqft__lte=sqrt)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'district_choices': list(districts),
        'sqrt_choices': sqrt_choices,
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
            listing = Listing(realtor=realtor, address=location, district=district,
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


def data_mining(request):
    """
    This function use tf-idf to calculate the 5 relate real-estate
    :param request:
    :return:
    """
    query_list = Listing.objects.all().order_by('id')
    all_data = ['' for i in range(len(query_list.values()))]
    for data in query_list.values():
        print(data['id'])
        print(f'relate_real_estate {data["relate_real_estate"]}')
        all_data[data['id'] - 1] = data['title'] + " " + str(data['price']) + " " + data['address'] + data[
            'description']
    print(f'len {len(all_data)}')
    relate_real_esate = []
    tfidf = TfidfVectorizer().fit_transform(all_data)

    for i in range(0, len(all_data) - 1):
        cosine_similarities = linear_kernel(tfidf[i:i + 1], tfidf).flatten()
        relate_real_esate.append(cosine_similarities.argsort()[:-5:-1])
        list_ids = ""
        for value in cosine_similarities.argsort()[:-5:-1]:
            list_ids = list_ids + str(value) + ","
        list_ids.lstrip(",")
        print(list_ids)
        Listing.objects.filter(id=i+1).update(relate_real_estate=list_ids)
    return render(
        request, "admin/base_site.html"
    )
