from django.urls import path

from .views import index_view, ask_view, upload_json

urlpatterns = [
    path('', index_view, name='index'),
    path('ask/', ask_view, name='ask'),
    path('upload_json/', upload_json, name='upload_json'),
]