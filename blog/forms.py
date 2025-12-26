from django import forms
from .models import Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Enter a valid email address."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Custom help texts
        self.fields['username'].help_text = "Choose a unique username."
        self.fields['password1'].help_text = "Use at least 8 characters, including letters and numbers."
        self.fields['password2'].help_text = "Enter the same password as above for verification."
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
           # 'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }
