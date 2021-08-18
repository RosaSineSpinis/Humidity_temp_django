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
    # simple set of data plot to matplotlib
    # path('charts/simple/', simple, name='simple'),
    # matplotlib version
    path('charts/plot_matlib/', plot_matlibplot_all, name='plot_matplotlib_all'),
    # similar to the final
    # path('charts/chart_data/', Plot_chart_js.as_view(), name='plot_chart_js'),
    # charts/plot_chart_js/ is waiting to be linear - probably not really needed
    # path('charts/plot_chart_js/', HomeView.as_view(), name='plot_chart_js'),
    path('charts/plot_charts/', ShowChart.as_view(), name='show_menu'),

]

#dataAnalysisTool/charts/simple/