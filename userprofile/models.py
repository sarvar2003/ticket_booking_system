# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


from userprofile.managers import UserProfileManager


# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    first_name = models.CharField(_("First name"), max_length=30, blank=True)
    last_name = models.CharField(_("Last name"), max_length=30, blank=True)
    username = models.CharField(
        _("Username"),
        max_length=150,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        blank=True,
        null=True,
    )
    email = models.EmailField(
        _("Email"),
        unique=True,
        max_length=200,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    is_active = models.BooleanField(_("Status"), default=True)
    # to verify users by email
    is_verified = models.BooleanField(_("Status"), default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)
    USERNAME_FIELD = "email"
    objects = UserProfileManager()


    class Meta:
        verbose_name = "UserProfile"
        verbose_name_plural = "UserProfiles"

    def __str__(self):
        return self.username or self.email