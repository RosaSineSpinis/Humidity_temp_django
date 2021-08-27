from django.shortcuts import render, redirect

# Create your views here.

import random
import django
import datetime
from .functions import ProcessDataFromDjango, Plotter
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import time
from pprint import pprint
from json import dumps

from django.views.generic import View
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import requests
import json

# @require_http_methods(["GET", "POST"])
# def demographics(request):
#
#     if request.method == 'POST':
#         route = request.POST.get('dataset')
#         label = request.POST.get('label')
#
#         '''get data'''
#         # text_l, text_v, text_c = text_demographics(route, label, vectorizer='count')
#         '''get data'''
#         # tfidf_l, tfidf_v, tfidf_c = text_demographics(route, label, vectorizer='tfidf')
#         '''get dates'''
#         created = creation_date_demographics(route, label)
#         '''get hash tags'''
#         # hashtag_labels, hashtag_values, hashtag_palette = hashtag_demographics(route, label)
#         '''get data about users'''
#         # users_labels, users_values, palette = user_demographics(route, label)
#         '''there is no function'''
#         # demographics_ctx = demographics_info(route, label)
#
#         '''I think we make whole page here'''
#         content = render_to_string("includes/demographics.html", demographics_ctx)
#         '''similary here'''
#         msg = render_to_string("includes/message.html", {"tags": "success", "message": "Demographics loaded"})
#         '''dictionary of all data'''
#         response = {
#             "demographics": content,
#             "msg": msg,
#             # "doughnut": [users_labels, users_values, palette],
#             # "hashtag": [hashtag_labels, hashtag_values, hashtag_palette],
#             "creation": created,
#             # "words": [text_l, text_v, text_c],
#             # "tfidf": [tfidf_l, tfidf_v, tfidf_c]
#         }
#         '''json return but to what??'''
#         return JsonResponse(response)
#
#     return render(request, 'chart_js_linear2.html', {})


def simple(request):
    ''' example function with matlib'''
    df = ProcessDataFromDjango.process_data()

    fig = Figure()
    ax = fig.add_subplot(111)
    x = []
    y = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now += delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


def plot_matlibplot_all(request):
    # think to add range of data to processing data
    df = ProcessDataFromDjango.process_data()
    fig = Plotter().plotAllInOne(['H1', 'H2', 'H3', 'H4'], ['H1', 'H2', 'H3', 'H4'], df, 'Humidity', '%')
    fig.autofmt_xdate()
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class Plot_chart_js(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        created to plot humidity and temperature as a variable of time
        :param request:
        :return: return data to plot in linear graph
        """
        df = ProcessDataFromDjango.process_data()
        # print('type', df.dtypes)

        x_name = list(df.keys())[-1]

        df.iloc[:, -1] = [int(time.mktime(t.timetuple())) * 1000 for t in df.iloc[:, -1] if t]

        list_of_data = []
        colors = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ]

        for idx, col in enumerate(df.columns):
            if idx == len(df.columns) - 1:
                break

            df_new = df.loc[:, [col, 'Date_time']]
            df_new.columns = ['y', 'x']
            df_new = df_new.to_dict(orient="records")

            list_of_data.append({'data': df_new, 'color': colors[idx], 'name': col})

            # pprint(list_of_data)

        data_series = {'all_series': list_of_data}
        # data_series = json.dumps(all_series)

        data = df.to_dict(orient='records')


        borderColor = [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
        ]

        # 'rgba(153, 102, 255, 0.6)',
        # 'rgba(255, 159, 64, 0.6)',
        # 'rgba(255, 99, 132, 0.6)'
        # print('x_name', x_name)

        # data = {
        #     "data_series": data_series,
        #     # "borderColor": borderColor,
        #     # "fill": False}
        # }
        # data_series = {'a': 1,
        #                'b': 2}
        return Response(data_series)


class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'chart_js_linear.html', {})


def show_menu(request):

    return render(request, 'menu_menu.html', {})


class ShowChart(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        """
        created to plot humidity and temperature as a variable of time
        :param request:
        :return: return data to plot in linear graph
        """
        is_loaded_data = 1  # set parameter in post in template

        dataset_kind = request.POST.get('dataset')
        print(dataset_kind)

        df_hum, df_temp = ProcessDataFromDjango.process_data(is_loaded_data)

        if dataset_kind == "humidity":
            data_series = ProcessDataFromDjango.prepare_data_to_chart_js(df_hum) #returns dictionary
        else:
            data_series = ProcessDataFromDjango.prepare_data_to_chart_js(df_temp) #returns dictionary
            print(df_temp)

        return Response(data_series)

    def get(self, request, format=None):

        return render(request, 'chart_menu.html', {})


class ShowChart_test(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []



    def get(self, request, format=None):
        df_hum, df_temp = ProcessDataFromDjango.process_data()
        data_series = ProcessDataFromDjango.prepare_data_to_chart_js(df_hum)  # returns dictionary
        return Response(data_series)

