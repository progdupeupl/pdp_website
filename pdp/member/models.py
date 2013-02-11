# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from hashlib import md5

from pdp.forum.models import Post, Topic       

class Profile(models.Model):
    '''Classe représentant un profil d'utilisateur'''
    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    user = models.ForeignKey(User, unique=True, verbose_name='Utilisateur')

    site = models.CharField('Site internet', max_length=128, blank=True)
    show_email = models.BooleanField('Afficher adresse mail publiquement', \
                 default=True)

    biography = models.TextField('Biographie', blank=True)

    def __unicode__(self):
        '''Représentation textuelle d'un profil'''
        return self.user.username

    def get_absolute_url(self):
        '''URL absolue vers la page du profil'''
        return '/membres/voir/%s' % self.user.username

    def get_gravatar_url(self):
        '''URL vers l'image du profil via Gravatar'''
        return 'http://gravatar.com/avatar/%s?d=identicon' % md5(self.user.email).hexdigest()

    def get_post_count(self):
        '''Nombre de messages postés sur le forum'''
        return Post.objects.all().filter(author__pk=self.user.pk).count()

    def get_topic_count(self):
        '''Nombre de sujets créés sur le forum'''
        return Topic.objects.all().filter(author__pk=self.user.pk).count()
