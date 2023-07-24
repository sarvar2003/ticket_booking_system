from django.contrib.auth.base_user import BaseUserManager


class UserProfileManager(BaseUserManager):
    """
    Customer user manager for Unaeon.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password
        """
        if not email:
            raise ValueError("Unaeon users must have an email address")

        user = self.model(email=UserProfileManager.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and save a Superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return
