from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
User=get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email',)

    password1=forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label=' Confirm Password')


    def  clean_password(self):
        password1=self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password12')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError('password must match')
        return password2

    def save(self,commit=True):
        user=super(UserAdminCreationForm, self).save( commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    email=forms.EmailField()


class LoginForm(forms.Form):
    email=forms.EmailField(max_length=250)
    password=forms.CharField(max_length=250,widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email',)

    password1=forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label=' Confirm Password')


    def  clean_password(self):
        password1=self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password12')
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError('password must match')
        return password2

    def save(self,commit=True):
        user=super(RegisterForm, self).save( commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=250)
#     email=forms.EmailField()
#     password = forms.CharField(max_length=250, widget=forms.PasswordInput)
#     password2 = forms.CharField(label='confirm password',max_length=250, widget=forms.PasswordInput)
#
#     def clean_username(self):
#         username=self.cleaned_data.get('username')
#         qs=User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError('username is taken')
#         else:
#             return username
#
#     def clean(self):
#         data=self.cleaned_data
#         password=self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#         if (password!=password2):
#             raise forms.ValidationError('password must match')
#         else:
#             return data

