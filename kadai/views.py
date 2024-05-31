from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Kadai
from .forms import SearchForm
from django.urls import reverse_lazy
from django import forms
from django.shortcuts import render


import re
import sys
import requests
import pandas as pd
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
    success_url = reverse_lazy('kadai:search_result')

    def form_valid(self, form):
        kadai = form.save(commit=False)
        kadai.user = self.request.user
        kadai.save()
        return super().form_valid(form)

class SearchResultView(generic.FormView):
    template_name = 'search_result.html'
    form_class = SearchForm
    model = Kadai

    def post(self, request, *args, **kwargs):
        context = {}
        form = self.get_form()
        if form.is_valid():
            year = request.POST.get('year')
            month = request.POST.get('month')
            words = request.POST.get('words')

            #総理の1か月
            def PrimeMinister_month(year, month, words):
                ## URLの場合分け
                # 　〇〇代総理を期間で分ける
                souri_url = ''
                if datetime(2017, 11, 1) <= datetime(int(year), int(month), 1) <= datetime(2020, 9, 1):
                    souri_url = '98_abe'
                elif datetime(2020, 10, 1) <= datetime(int(year), int(month), 1) <= datetime(2021, 9, 1):
                    souri_url = '99_suga'
                elif (int(year) == 2021) and (int(month) == 10):
                    souri_url = '100_kishida'
                else:
                    souri_url = '101_kishida'

                # 「月」が1～9月なら、前に0をつける（「202404」のようにしたい）
                scp_url = ''
                if re.match(r'^[1-9]$', month):
                    scp_url = "https://www.kantei.go.jp/jp/" + souri_url + "/actions/" + str(year) + '0' + str(
                        month) + "/index.html"
                else:
                    scp_url = "https://www.kantei.go.jp/jp/" + souri_url + "/actions/" + str(year) + str(
                        month) + "/index.html"

                # スクレイピングを行うWEBサイトからHTMLをレスポンスさせる
                res = requests.get(scp_url)
                res.encoding = res.apparent_encoding

                # bsオブジェクトを作る
                soup = BeautifulSoup(res.text, 'html.parser')

                # 日付、タイトル、本文を抜き出す
                date_list = soup.find_all('div', class_='news-list-date')
                title_list = soup.find_all('div', class_='news-list-title')
                body_list = soup.find_all('div', class_='news-list-text')


                month_list = []
                # １つのリストにまとめる
                for i, j in enumerate(date_list):
                    day = re.search(r'月(.+)日', j.text).group(1)
                    title = title_list[i].text.replace('　', '').replace('\n', '').replace('\r', '')
                    body = body_list[i].text.replace('　', '').replace('\n', '').replace('\r', '')
                    # wordsが含まれるか
                    if words in title or words in body:
                        month_list.append([year, month, int(day), title, body])

                month_list.sort()
                df = pd.DataFrame(month_list, columns=['年', '月', '日', 'タイトル', '概要'])
                return df

            #支持率
            def Approval_Rating(year, month):
                # 「月」が1～9月なら、前に0をつける（「202404」のようにしたい）。直接指定は選挙の為
                scp_url = ''
                if (year=='2021') and (month=='10'):
                    scp_url = 'https://www.nhk.or.jp/senkyo/shijiritsu/archive/2021/10_1.html'
                elif (year=='2022') and (month=='6'):
                    scp_url = 'https://www.nhk.or.jp/senkyo/shijiritsu/archive/2022/06_1.html'
                elif re.match(r'^[1-9]$', month):
                    scp_url = 'https://www.nhk.or.jp/senkyo/shijiritsu/archive/' + year + '/0' + month + '.html'
                else:
                    scp_url = 'https://www.nhk.or.jp/senkyo/shijiritsu/archive/' + year + '/' + month + '.html'

                print(scp_url)
                # スクレイピングを行うWEBサイトからHTMLをレスポンスさせる
                res = requests.get(scp_url)
                res.encoding = res.apparent_encoding

                # bsオブジェクトを作る
                soup = BeautifulSoup(res.text, 'html.parser')

                lead = soup.find(class_='no-border lead')
                rate = lead.find('h3')

                return rate.text


            #当該月のニュース
            def month_news(year, month):
                # 2019年以降からURLが変わる
                if int(year) >= 2019:
                    url_head = 'https://www.nippon.com/ja/news/q'
                else:
                    url_head = 'https://www.nippon.com/ja/features/q'

                # 「月」が1～9月なら、前に0をつける（「202404」のようにしたい）
                scp_url = ''
                if re.match(r'^[1-9]$', month):
                    scp_url = url_head + str(year) + '0' + str(month)
                else:
                    scp_url = url_head + str(year) + str(month)

                # スクレイピングを行うWEBサイトからHTMLをレスポンスさせる
                res = requests.get(scp_url)
                res.encoding = res.apparent_encoding

                # bsオブジェクトを作る
                soup = BeautifulSoup(res.text, 'html.parser')

                page = soup.find(class_='editArea')

                news_list = []
                for news in page.find_all(['h3', 'p'], class_=None):
                    if ('バナー写真' in news.text) == False:
                        news_list.append(news.text)

                return news_list

            # コンテキストにデータを格納
            context['rate'] = Approval_Rating(year, month)
            context['PrimeMinister_month'] = PrimeMinister_month(year, month, words)
            context['news'] = month_news(year, month)
            context['year'] = year
            context['month'] = month

            kadai = form.save(commit=False)
            kadai.user = request.user
            kadai.save()

            return render(request, 'search_result.html', context)

        return self.form_invalid(form)