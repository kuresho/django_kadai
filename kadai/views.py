from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Kadai
from .forms import SearchForm
from django.urls import reverse_lazy
from django import forms


import re
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class IndexView(generic.TemplateView):
    template_name = "index.html"

class SearchLogView(LoginRequiredMixin,generic.ListView):
    model = Kadai
    template_name = 'search_log.html'

    def get_queryset(self):
        Logs = Kadai.objects.filter(user=self.request.user).order_by('-search_at')
        return Logs

class SearchView(LoginRequiredMixin,generic.CreateView):
    model = Kadai
    template_name = 'search.html'
    form_class = SearchForm
    success_url = reverse_lazy('kadai:kadai_list')
    
    def form_valid(self, form):
        kadai = form.save(commit=False)
        kadai.user = self.request.user
        kadai.save()


    def SearchResult(request):
        if request.method == "POST":
            year = request.POST['year']
            month = request.POST['month']
            return render(request, 'search_result.html', year)


class SearchResultView(generic.TemplateView):
    template_name = 'search_result.html'
