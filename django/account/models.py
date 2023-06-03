from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db.models.functions import Upper
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class UserRole(models.Model):
    """
    Role for each user, e.g. Admin, Collaborator
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        """
        Allow users to login with case-insensitive username

        E.g. both "My.Name@uni.ac.uk" and "my.name@uni.ac.uk" will allow users to login
        """
        return self.get(username__iexact=username)


class User(AbstractUser):
    """
    Custom user extends the standard Django user model, providing additional properties
    """

    objects = CustomUserManager()  # Custom user manager used to allow for case-insensitive usernames

    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def name(self):
        if self.first_name and self.last_name:
            return ' '.join((self.first_name, self.last_name))
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            # If no first or last name provided, return first half of email
            return self.username.split('@')[0]  # e.g. mike.allaway in mike.allaway@ox.ac.uk

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Force email and username to be lower case and identical, so users can login with email
        self.email = self.email.strip().lower()
        self.username = self.email

        # User Roles (to be used below)
        role_admin = UserRole.objects.get(name='admin')
        role_collaborator = UserRole.objects.get(name='collaborator')

        # Set a default role for new users (with lowest permissions)
        if not self.role:
            self.role = role_collaborator

        # Set values for each user role:
        # Admins (full control)
        if self.role == role_admin:
            self.is_staff = True
            self.is_superuser = True
        # Collaborators (limited control)
        elif self.role == role_collaborator:
            self.is_staff = True
            self.is_superuser = False

        # Get old role (before this change)
        if self.id:
            old_role = User.objects.get(id=self.id).role
            # If changing role to an admin (i.e. from a collaborator), email the admin
            if old_role != role_admin and self.role == role_admin:
                # Send email alert to research team
                try:
                    send_mail('Invisible East: New Admin User',
                              f"A user ({ self.name } - { self.username }) has been made an Admin of the Invisible East database. If you recognise this person then you can ignore this email. If you don't recognise this person then please email: {settings.EMAIL_HOST_USER} immediately.",
                              settings.DEFAULT_FROM_EMAIL,
                              (settings.MAIN_CONTACT_EMAIL,),
                              fail_silently=False)
                except Exception:
                    logger.exception("Failed to send email")

        # If no user with an admin role exists (i.e. this is the first user being added to the database)
        # then set this user as an admin, as there must be at least 1 admin
        if User.objects.filter(role=role_admin).count() == 0:
            self.role = role_admin
            self.is_staff = True
            self.is_superuser = True

        super().save(*args, **kwargs)

        # Once user is saved, add to necessary permission group
        # collaborator_permissions_group
        if self.role == UserRole.objects.get(name='collaborator'):
            Group.objects.get(name='collaborator_permissions_group').user_set.add(self)

    class Meta:
        ordering = [Upper('email'), 'id']