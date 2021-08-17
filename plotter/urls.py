from django.urls import path, include

from plotter.views import(
    getGraph,
)


app_name = 'plotter'

urlpatterns = [
    path('graph/', getGraph, name='plot_mat_lib'),
]
