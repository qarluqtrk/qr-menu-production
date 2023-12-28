from django.shortcuts import render

from app.utils.poster import poster


def index_view(request):
    categories = poster.get_categories()
    return render(request, 'app/index.html',
                  {'categories': categories})
