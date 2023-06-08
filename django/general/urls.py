from django.urls import path
from . import views

app_name = 'general'

urlpatterns = [
    path('', views.WelcomeTemplateView.as_view(), name='welcome'),

    path('about/cite/', views.AboutCiteTemplateView.as_view(), name='about-cite'),
    path('about/credits/', views.AboutCreditsTemplateView.as_view(), name='about-credits'),
    path('about/faqs/', views.AboutFaqsTemplateView.as_view(), name='about-faqs'),
    path('about/glossary/', views.AboutGlossaryTemplateView.as_view(), name='about-glossary'),
    path('about/resources/', views.AboutResourcesTemplateView.as_view(), name='about-resources'),
    path('about/technical/', views.AboutTechnicalTemplateView.as_view(), name='about-technical'),

    path('accessibility/', views.AccessibilityTemplateView.as_view(), name='accessibility'),
    path('cookies/', views.CookiesTemplateView.as_view(), name='cookies'),

    path('robots.txt', views.RobotsTemplateView.as_view(), name='robots')
]
