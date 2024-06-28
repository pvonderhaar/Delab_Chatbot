from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Create your views here.
from django.http import HttpResponse
from .utils import download


def index(request):
    return render(request, 'download/download_temp.html')


@csrf_exempt
@require_POST
def ask_view(request):
    # TODO: Bessere answer wiedergeben
    user_input = request.POST.get('user_input')
    answer = download(user_input)
    return JsonResponse({'answer': answer})