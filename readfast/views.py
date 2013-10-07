from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from readfast.models import Test

class TestIndexView(View):
    def get(self, request, *args, **kwargs):
        test_list = Test.objects.order_by('-id')
        return render(request, 'readfast/index.html', {'test_list': test_list})

class TestDetailView(View):
    def get(self, request, test_id, *args, **kwargs):
        test = get_object_or_404(Test, pk=test_id)
        return render(request, 'readfast/detail.html', {'test': test})