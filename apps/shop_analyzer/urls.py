from django.urls import path

from . import views

urlpatterns = (
    path('', views.home, name='home'),
    path('get-data/<int:s_pk>/', views.get_data, name='get_data'),
)
