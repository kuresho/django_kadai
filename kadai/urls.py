from django.urls import path

from . import views

app_name = 'kadai'
urlpatterns = [
    path('',views.IndexView.as_view(),name="index"),
    path('search-log/',views.SearchLogView.as_view(),name="search_log"),
    path('search-result',views.SearchResultView.as_view(),name='search_result'),
    path('search/',views.SearchView.as_view(),name='search'),
]