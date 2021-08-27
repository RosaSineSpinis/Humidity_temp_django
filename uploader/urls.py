from django.conf.urls import url
from django.urls import path, include

from uploader.views import(
    list_view,
    FileFieldFormView,
    directory_load_view,
)


app_name = 'uploader'

urlpatterns = [
    path('load/', list_view, name='list'),
    path('load_multiple/', FileFieldFormView.as_view(), name='multiple_load'),
    path('load_directory/', directory_load_view, name='directory_load')
]

# uploader/load_directory/