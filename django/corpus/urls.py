from django.urls import path
from . import views

app_name = 'corpus'

urlpatterns = [

    # Text
    path('', views.TextListView.as_view(), name='text-list'),
    path('<pk>/', views.TextDetailView.as_view(), name='text-detail'),

    # TextFolioTag
    path('textfoliotag/create/', views.TextFolioTagCreateView.as_view(), name='textfoliotag-create'),
    path('textfoliotag/failed/', views.TextFolioTagFailedTemplateView.as_view(), name='textfoliotag-failed'),

    # TextFolioTransLineDrawnOnImage
    path('textfoliotranslinedrawnonimage/manage/', views.TextFolioTransLineDrawnOnImageManageView.as_view(), name='textfoliotranslinedrawnonimage-manage'),
    path('textfoliotranslinedrawnonimage/failed/', views.TextFolioTransLineDrawnOnImageFailedTemplateView.as_view(), name='textfoliotranslinedrawnonimage-failed'),

    # Maps
    path('map/tagged-texts/', views.MapTaggedTextsListView.as_view(), name='map-taggedtexts'),
    path('map/find-spots/', views.MapFindSpotTemplateView.as_view(), name='map-findspots'),
    path('map/places-in-texts/', views.MapPlacesMentionedInCorpusTextsTemplateView.as_view(), name='map-placesintexts'),

]
