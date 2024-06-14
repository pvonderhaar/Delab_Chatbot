from django.urls import path

from .views import index_view, ask_view

urlpatterns = [
    path('', index_view, name='index'),
    path('ask/', ask_view, name='ask'),
]