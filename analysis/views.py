from django.shortcuts import render
import random
from listings.models import Listing


def index(request):
    """
    index function to draw chart about listing
    :param request:
    :return:
    """

    queryset_list = Listing.objects.order_by('-price')
    districts = Listing.objects.order_by('district').distinct().values_list('district', flat=True)
    if 'district' in request.GET:
        district = request.GET['district']
        if district:
            queryset_list = queryset_list.filter(district=district)

    # print(list(queryset_list))
    count = 0
    labels = []
    datas = []
    labels_pie = ['Thấp hơn 5 (triệu/m²)', 'Từ 5 đến 10 (triệu/m²)', 'Từ 10 đến 20 (triệu/m²)',
                  'Từ 20 đến 30 (triệu/m²)', 'Từ 30 đến 50 (triệu/m²)', 'Trên 50 (triệu/m²)']
    datas_pie = [0, 0, 0, 0, 0, 0]

    for data in list(queryset_list):
        if data.price != 0 and data.price < 300:
            labels.append(count)
            count = count + 1
            datas.append(data.price)
            if data.price <= 5:
                datas_pie[0] += 1
            elif 5 < data.price <= 10:
                datas_pie[1] += 1
            elif 10 < data.price <= 20:
                datas_pie[2] += 1
            elif 20 < data.price <= 30:
                datas_pie[3] += 1
            elif 30 < data.price <= 50:
                datas_pie[4] += 1
            else:
                datas_pie[5] += 1

    context = {
        'district_choices': list(districts),
        'labels': labels,
        'data': datas,
        'labels_pie': labels_pie,
        'datas_pie': datas_pie,
        'values': request.GET,
    }
    return render(request, 'analysis/analysis.html', context)
