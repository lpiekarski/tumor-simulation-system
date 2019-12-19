from django.shortcuts import render
from django.http import HttpResponse
from homepage.models import Carousel


def homepage(request, template_name="homepage.html"):
    context = {'carousel_items': Carousel.objects.all().filter(is_public=True)}
    return render(request, template_name, context)


def error_500_view(request):
    with open("templates/500.html") as f:
        text = f.read()
    response = HttpResponse(text)
    response.status_code = 500
    return response


def error_404_view(request):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def health_check_view(request):
    return HttpResponse("ok")
