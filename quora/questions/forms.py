from django import forms
from quora.questions.models import Question

QUESTION_PLACEHOLDER = 'Which pair of hiking shoes are best for bay area hikes?'
SUMMARY_PLACEHOLDER = 'Details go here.'
TAG_PLACEHODER = 'hiking shoes'


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control input-lg',
            'placeholder': QUESTION_PLACEHOLDER,
        }),
        max_length=255,
        label='No-show',)
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control', 'placeholder': SUMMARY_PLACEHOLDER}),
        max_length=4000,
        required=False,
        label='No-show')
    tags = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': TAG_PLACEHODER}),
        max_length=255,
        required=False,
        label='tags',
        help_text='Use spaces to separate tags')

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags', 'status']
