from django.shortcuts import render
import random


def index(request):
    """
    index function to draw chart about listing
    :param request:
    :return:
    """
    labels = [u"Quốc Oai", u"Thạch thất", "Chương Mỹ", "Ba Vì"]
    data = [2, 1.5, 3, 5]
    for i in range(0, 100):
        labels.append("Ba vì {0}".format(i))
        data.append(random.randint(4, 10))

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'analysis/analysis.html', context)
