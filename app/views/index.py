from django.shortcuts import render

from app.utils.poster import poster


def index_view(request):
    categories = poster.get_categories()
    return render(request, 'app/index.html',
                  {'categories': categories})


def bad_request_view_custom(request, exception=None):
    return render(request, 'app/bad-request.html')
