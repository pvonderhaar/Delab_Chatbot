from django.shortcuts import render
# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .utils import generate_answer, get_context


def index_view(request):
    request.session['context'] = get_context()
    context = request.session['context']
    return render(request, 'chatbot/chat_temp.html', {'context_items': context.items()})


@csrf_exempt
@require_POST
def ask_view(request):
    user_input = request.POST.get('user_input')
    context = request.session.get('context', get_context())
    answer = generate_answer(user_input, context)
    return JsonResponse({'answer': answer})