from django.views.generic import TemplateView


class WelcomeTemplateView(TemplateView):
    """
    Class-based view to show the welcome template
    """
    template_name = 'general/welcome.html'


class AboutTemplateView(TemplateView):
    """
    Class-based view to show the about template
    """
    template_name = 'general/about.html'


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
