from django.shortcuts import render


def vue(request):
    return render(request, 'frontend.html', {})
