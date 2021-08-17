from django.urls import path, include

from .views import simple,\
                   plot_matlibplot_all,\
                   Plot_chart_js, \
                    show_menu, \
                    HomeView, \
                    ShowChart
                    # demographics,\


app_name = 'dataAnalysisTool'
urlpatterns = [
    path('charts/simple', simple, name='simple'),
    path('charts/plot_matlib', plot_matlibplot_all, name='plot_matplotlib_all'),
    path('charts/chart_data/', Plot_chart_js.as_view(), name='plot_chart_js'),
    # path('charts/demographics/', demographics, name='demographics'),
    path('charts/plot_chart_js/', HomeView.as_view(), name='plot_chart_js'),
    path('charts/plot_charts/', ShowChart.as_view(), name='show_menu')

]

