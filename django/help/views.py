from django.views.generic import (DetailView, ListView)
from django.db.models import Q
from . import models


def help_queryset(self):
    """
    Applies required filtering for Help objects
    To be used in below get_queryset() methods
    """

    # Only ever show published objects
    queryset = self.model.objects.filter(admin_published=True)

    # If user is logged in, only show help items if 'visible_only_to_user_groups' is
    # None or the current user's role
    if self.request.user.is_authenticated:
        queryset = queryset.filter(
            Q(visible_only_to_user_groups=None) |
            Q(visible_only_to_user_groups__id=self.request.user.role.id)
        )
    # If user is not logged in, only show help items if no roles specified in 'visible_only_to_user_groups'
    else:
        queryset = queryset.filter(visible_only_to_user_groups=None)

    return queryset


class HelpDetailView(DetailView):
    """
    Class-based view for help detail template
    """
    template_name = 'help/detail.html'
    model = models.HelpItem

    def get_queryset(self):
        return help_queryset(self)


class HelpListView(ListView):
    """
    Class-based view for help list template
    """
    template_name = 'help/list.html'
    model = models.HelpItem

    def get_queryset(self):
        return help_queryset(self)
