# coding: utf-8

from os import path

from django.db import models
from django.contrib.auth.models import User

from pdp.utils import slugify

# Les classes sont organisées de façon à avoir la structure suivante :
#
# - Pour les big-tutos : Tutorial < Parts < Chapters
# - Pour les mini-tutos : Tutorial < Chapter

def tutorial_icon_path(instance, filename):
    return 'tutoriels/tutoriels/%s%s' % \
            (instance.pk, path.splitext(filename)[1])

def part_icon_path(instance, filename):
    return 'tutoriels/parties/%s%s' % \
            (instance.pk, path.splitext(filename)[1])

def chapter_icon_path(instance, filename):
    return 'tutoriels/chapitres/%s%s' % \
            (instance.pk, path.splitext(filename)[1])

class Tutorial(models.Model):
    '''Classe représentant un tutoriel'''
    class Meta:
        verbose_name = 'Tutoriel'
        verbose_name_plural = 'Tutoriels'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)
    authors = models.ManyToManyField(User, verbose_name='Auteurs')

    icon = models.ImageField(upload_to=tutorial_icon_path, \
        null=True, blank=True)

    # On pourrait distinguer les mini des big tutos en parcourant la base
    # et en retrouvant les chapitres qui sont directement associés à un
    # tutoriel mais ce serait sans doute plus long qu'un simple champ
    is_mini = models.BooleanField('Est un mini-tutoriel')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/tutoriels/voir/%s-%s/' % (self.pk, slugify(self.title))

    def get_parts(self):
        return Part.objects.all()\
            .filter(tutorial__pk=self.pk)\
            .order_by('position_in_tutorial')

def get_last_tutorials():
    # TODO: ranger par date de mise en ligne (ou mise à jour ?)
    return Tutorial.objects.all().order_by('title')[:3]

    def get_chapter(self):
        '''Retourne le chapitre associé au mini-tutoriel'''
        # On peut utiliser get car on est sûr qu'un seul chapitre sera
        # directement associé à ce mini-tutoriel
        return Chapter.objects.get(tutorial__pk=self.pk)

class Part(models.Model):
    '''Classe représentant un groupement de chapitres'''
    class Meta:
        verbose_name = 'Partie'
        verbose_name_plural = 'Parties'

    # Une partie possède nécessairement un tutoriel parent, étant donné que
    # seul les tutoriels avec parties sont des big-tutos
    tutorial = models.ForeignKey(Tutorial, verbose_name='Tutoriel parent')
    position_in_tutorial = models.IntegerField('Position dans le tutoriel')

    title = models.CharField('Titre', max_length=80)

    introduction = models.TextField('Introduction')
    conclusion = models.TextField('Conclusion')

    # Entre l'introduction et la conclusion des parties se trouveront la liste
    # des chapitres associés

    def __unicode__(self):
        return '<Partie pour %s, %s>' % \
            (self.tutorial.title, self.position_in_tutorial)

    def get_absolute_url(self):
        return self.tutorial.get_absolute_url() + '%s-%s/' % (\
            self.position_in_tutorial,
            slugify(self.title)
        )

    def get_chapters(self):
        return Chapter.objects.all()\
            .filter(part=self).order_by('position_in_part')

class Chapter(models.Model):
    '''Classe représentant un chapitre de tutoriel dans lequel se situe l'info
    rmation'''
    class Meta:
        verbose_name = 'Chapitre'
        verbose_name_plural = 'Chapitres'

    # Une partie possède accessoirement un chapitre parent, c'est la que se
    # fait la différenciation entre les big et mini-tutoriels
    part = models.ForeignKey(Part, null=True, blank=True,\
        verbose_name='Partie parente')

    position_in_part = models.IntegerField('Position dans la partie',\
        null=True, blank=True)
    
    # Si le chapitre n'est pas relié à une partie particulière, c'est alors
    # que c'est un mini-tutoriel ; il faut donc le relier à des informations
    # concernant ce même tutoriel directement
    tutorial = models.ForeignKey(Tutorial, null=True, blank=True,\
        verbose_name='Tutoriel parent')
    
    title = models.CharField('Titre', max_length=80, blank=True)

    introduction = models.TextField('Introduction')
    conclusion = models.TextField('Conclusion')

    def __unicode__(self):
        if self.tutorial:
            return u'<minituto \'%s\'>' % self.tutorial.title
        elif self.part:
            return u'<bigtuto \'%s\', \'%s\'>' % \
                (self.part.tutorial.title, self.title)
        else:
            return u'<orphelin>'

    def get_absolute_url(self):
        # Si le chapitre est un mini-tuto
        if self.tutorial:
            return self.tutorial.get_absolute_url()

        # Si le chapitre fait parti d'un big-tuto
        elif self.part:
            return self.part.get_absolute_url() + '%s-%s' % (
                self.position_in_part,
                slugify(self.title)
            )

        # Sinon, le chapitre n'a pas lieu d'être
        else:
            return redirect('/tutoriels/')

    def get_extract_count(self):
        return Extract.objects.all().filter(chapter__pk=self.pk).count()

    def get_extracts(self):
        return Extract.objects.all().filter(chapter__pk=self.pk)

class Extract(models.Model):
    '''Classe représentant un morceau de contenu dans un chapitre'''
    class Meta:
        verbose_name = 'Extrait'
        verbose_name_plural = 'Extraits'

    title = models.CharField('Titre', max_length=80)
    chapter = models.ForeignKey(Chapter, verbose_name='Chapitre parent')
    position_in_chapter = models.IntegerField('Position dans le chapitre')
    text = models.TextField('Texte')

    def get_absolute_url(self):
        return '%s#%s-%s' % (\
            self.chapter.get_absolute_url(),
            self.position_in_chapter,
            slugify(self.title)
        )
