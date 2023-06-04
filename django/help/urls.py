from django.urls import path
from . import views


app_name = 'help'

urlpatterns = [
    path('', views.HelpListView.as_view(), name='list'),
    path('<pk>/', views.HelpDetailView.as_view(), name='detail'),
]
