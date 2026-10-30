from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST

from .predictor import predict

MIN_LENGTH = 20


def clean_news(raw):
    news = (raw or '').strip()
    if len(news) < MIN_LENGTH:
        return None, f'Please enter at least {MIN_LENGTH} characters of news text.'
    return news, None


@require_http_methods(['GET', 'POST'])
def FND(request):
    if request.method == 'GET':
        return render(request, 'index.html')

    news, error = clean_news(request.POST.get('news'))
    if error:
        return render(request, 'index.html', {'error': error}, status=400)
    return render(request, 'index.html', {'result': predict(news), 'news': news})


@require_POST
def predict_api(request):
    news, error = clean_news(request.POST.get('news'))
    if error:
        return JsonResponse({'error': error}, status=400)
    return JsonResponse({'result': predict(news)})
