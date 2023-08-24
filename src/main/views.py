from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import get_quote, insert_quote, Quote
from django.views.generic import ListView

class QuoteView(ListView):
    template_name = 'index.html'
    model = Quote
    context_object_name = 'quotes'
    def get_queryset(self) -> QuerySet[Any]:
        return get_quote(self.request.GET.get('sort'))

def request_webpage(request): 
    context = get_quote(request.GET.get('sort'))
    return render(request, 'index.html', context) 

def create_quote(request):
    if request.method == 'POST':
        quote = request.POST.get('quote')
        author = request.POST.get('author')
        insert_quote(quote, author)
    
    sort_param = request.GET.get('sort', '') 
    if sort_param:
        return redirect('root', sort=sort_param)  # Redirect to the 'root' URL pattern with sort parameter
    else:
        return redirect('root') 