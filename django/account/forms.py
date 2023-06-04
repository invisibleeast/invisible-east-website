from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from .models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class PublicUserCreationForm(UserCreationForm):
    """
    Form to specify fields in the user creation form on the public website
    Role is ommitted as this will be set in the view, as users shouldn't choose their own role
    It's used in views.py
    """

    # Account Create Code (prevents unwanted people from creating account)
    account_create_code = forms.CharField(label='Account creation code',
                                          help_text="The code provided to you by the Invisible East team that's required to create an account. Contact us for help if you're unsure.")

    # Google ReCaptcha v3
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # removes : from label, e.g. Email: becomes Email
        self.fields['password1'].help_text = "Your password:<br>- can't be too similar to your other personal information.<br>- must contain at least 8 characters.<br>- can't be a commonly used password.<br>- can't be entirely numeric."

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('account_create_code', 'first_name', 'last_name', 'email',)

    def clean_account_create_code(self):
        """
        Ensure that the account_create_code matches the code defined in the settings. If not, show error.
        """
        cleaned_data = self.clean()
        account_create_code = cleaned_data.get('account_create_code')
        if account_create_code != settings.ACCOUNT_CREATE_CODE:
            self.add_error('account_create_code', "The account creation code is not valid")
        return account_create_code

    def clean_email(self):
        """
        Check that the email provided doesn't already exist
        """
        cleaned_data = self.clean()
        e = cleaned_data.get('email')
        # If this email exists
        if len(User.objects.filter(email=e)) > 0:
            self.add_error('email', "There's already an account associated with this email address")
        return e


class PublicUserChangeForm(UserChangeForm):
    """
    Form to specify fields in the user change form, which is accessible through the public website
    As users of different roles can use this form, 'role' field is excluded so they can't change their role
    It's used in views.py
    """

    # Hide password, as template gives a direct link to it styled more appropriately
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # removes : from label, e.g. Email: becomes Email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class PublicPasswordChangeForm(PasswordChangeForm):
    """
    Form to specify fields in the password change form, which is accessible through the public website
    It's used in views.py
    """

    # Hide password, as template gives a direct link to it styled more appropriately
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # removes : from label, e.g. Email: becomes Email
        self.fields['new_password1'].help_text = "Your password:<br>- can't be too similar to your other personal information.<br>- must contain at least 8 characters.<br>- can't be a commonly used password.<br>- cant be entirely numeric."

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
