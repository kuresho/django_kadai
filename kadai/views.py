from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Kadai


class IndexView(generic.TemplateView):
    template_name = "index.html"

class SearchLogView(LoginRequiredMixin,generic.ListView):
    model = Kadai
    template_name = 'search_log.html'

    def get_queryset(self):
        Logs = Kadai.objects.filter(user=self.request.user).order_by('-search_at')
        return Logs