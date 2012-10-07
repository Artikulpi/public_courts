from django import forms
from corruption.models import Case, Article, PollImprisonment, PollCriminalFines

class CaseForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = Case

class ArticleForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = Article

class PollImprisonmentForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = PollImprisonment
        fields = ('imprisonment',)
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.case = kewargs.pop('case', None)
        super(PollImprisonmentForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        poll = super(PollImprisonmentForm, self).save(commit=False)
        poll.user = self.request.user
        poll.case = self.case
        
        if commit:
            poll.save()
            
        return poll
    