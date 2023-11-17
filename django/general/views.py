from django.views.generic import TemplateView


class WelcomeTemplateView(TemplateView):
    """
    Class-based view to show the welcome template
    """
    template_name = 'general/welcome.html'


class AboutCiteTemplateView(TemplateView):
    """
    Class-based view to show the about-cite template
    """
    template_name = 'general/about-cite.html'


class AboutCreditsTemplateView(TemplateView):
    """
    Class-based view to show the about-credits template
    """
    template_name = 'general/about-credits.html'


class AboutFaqsTemplateView(TemplateView):
    """
    Class-based view to show the about-faqs template
    """
    template_name = 'general/about-faqs.html'


class AboutGlossaryTemplateView(TemplateView):
    """
    Class-based view to show the about-glossary template
    """
    template_name = 'general/about-glossary.html'


class AboutSearchTemplateView(TemplateView):
    """
    Class-based view to show the about-search template
    """
    template_name = 'general/about-search.html'


class AboutTechnicalTemplateView(TemplateView):
    """
    Class-based view to show the about-technical template
    """
    template_name = 'general/about-technical.html'


class AccessibilityTemplateView(TemplateView):
    """
    Class-based view to show the accessibility template
    """
    template_name = 'general/accessibility.html'


class CookiesTemplateView(TemplateView):
    """
    Class-based view to show the cookies template
    """
    template_name = 'general/cookies.html'


class RobotsTemplateView(TemplateView):
    """
    Robots: Template
    Class-based view to show the robots.txt file
    """
    template_name = 'general/robots.txt'
    content_type = 'text/plain'
