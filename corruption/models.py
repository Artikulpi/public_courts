from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    article_no = models.CharField(max_length=20)
    subject = models.TextField()
    imprisonment = models.CharField(max_length=10)
    criminal_fines = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'%s' % self.article_no
    
class Case(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    desc = models.TextField()
    images = models.ImageField(upload_to="photo")
    article_indictment = models.ManyToManyField(Article, blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.title
    
class Progress(models.Model):
    case = models.ForeignKey(Case)
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    desc = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.title
    
class Imprisonment(models.Model):
    case = models.ForeignKey(Case)
    desc = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s' % self.desc

class PollImprisonment(models.Model):
    user = models.ForeignKey(User)
    case = models.OneToOneField(Case)
    imprisonment = models.ForeignKey(Imprisonment)
    
    def __unicode__(self):
        return u'%s' % self.imprisonment
    
class CriminalFines(models.Model):
    case = models.ForeignKey(Case)
    desc = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s' % self.desc

class PollCriminalFines(models.Model):
    user = models.ForeignKey(User)
    case = models.OneToOneField(Case)
    criminal_fines = models.ForeignKey(CriminalFines)
    
    def __unicode__(self):
        return u'%s' % self.criminal_fines

class News(models.Model):
    case = models.ForeignKey(Case)
    title = models.CharField(max_length=100)
    news_url = models.URLField()
    date = models.DateField()
    short_desc = models.TextField()
    
    def __unicode__(self):
        return u'%s' % self.title
    