from django.urls import path
from . import views

app_name = 'researchdata'

urlpatterns = [
    path('', views.TextListView.as_view(), name='text-list'),
    path('<pk>/', views.TextDetailView.as_view(), name='text-detail')
]
