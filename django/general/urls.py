from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('', views.WelcomeTemplateView.as_view(), name='welcome'),
    path('about/', views.AboutTemplateView.as_view(), name='about'),

    path('accessibility/', views.AccessibilityTemplateView.as_view(), name='accessibility'),
    path('cookies/', views.CookiesTemplateView.as_view(), name='cookies'),

    path('robots.txt', views.RobotsTemplateView.as_view(), name='robots')
]
