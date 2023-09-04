from django.urls import path
from . import views

app_name = 'corpus'

urlpatterns = [
    # Text
    path('', views.TextListView.as_view(), name='text-list'),
    path('<pk>/', views.TextDetailView.as_view(), name='text-detail'),

    # TextFolioTag
    path('textfoliotag/manage/', views.TextFolioTagManageView.as_view(), name='textfoliotag-manage'),
    path('textfoliotag/failed/', views.TextFolioTagFailedTemplateView.as_view(), name='textfoliotag-failed'),

    # TextFolioTransLineDrawnOnImage
    path('textfoliotranslinedrawnonimage/manage/', views.TextFolioTransLineDrawnOnImageManageView.as_view(), name='textfoliotranslinedrawnonimage-manage'),
    path('textfoliotranslinedrawnonimage/failed/', views.TextFolioTransLineDrawnOnImageFailedTemplateView.as_view(), name='textfoliotranslinedrawnonimage-failed')
]
