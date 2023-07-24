from django import forms

class LoginForm(forms.Form):
    """ A form for user login 
    
    Attributes:
      username: A CharField representing the username input field.
      password: A CharField representing the password input field with a password widget.
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
