from django.db import models
from django.urls import reverse
from django.db.models.functions import Upper
from embed_video.fields import EmbedVideoField
from .apps import app_name
from account.models import UserRole


class HelpItem(models.Model):
    """
    A source of helpful information for using the website
    """

    name = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True, help_text='Must be a valid URL, e.g. https://www.ox.ac.uk')
    image = models.ImageField(upload_to='help-image', blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True, help_text='Provide a URL of a video hosted on YouTube or Vimeo, e.g. https://www.youtube.com/watch?v=BHACKCNDMW8')
    pdf = models.FileField(upload_to='help-pdf', blank=True, null=True)
    visible_only_to_user_groups = models.ManyToManyField(UserRole, blank=True, related_name='helpitems')

    # Admin
    admin_published = models.BooleanField(default=False, verbose_name='published')
    admin_notes = models.TextField(blank=True, null=True)

    @property
    def url_detail(self):
        return reverse(f'{app_name}:detail', kwargs={'pk': self.id})

    @property
    def list_title(self):
        return self.name

    @property
    def list_details(self):
        details = ''
        # Formats
        formats = []
        if self.pdf:
            formats.append('<i class="fas fa-file-alt"></i> PDF')
        if self.image:
            formats.append('<i class="fas fa-image"></i> Image')
        if self.link:
            formats.append('<i class="fas fa-link"></i> Link')
        if self.video:
            formats.append('<i class="fas fa-video"></i> Video')
        details = ' | '.join(formats)
        details += '<br>' if formats else ''  # Add a new line, if any formats have been added
        return details if len(details) < 700 else f'{details[0:697]}...'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('help:detail', args=[str(self.id)])

    class Meta:
        ordering = [Upper('name'), 'id']
