# coding: utf-8

from os import path

from django.db import models
from django.contrib.auth.models import User

from pdp.utils import slugify

# The class hierarchy is as follows :
# - "large" tutorials: Tutorial < Parts < Chapters
# - "small" tutorials : Tutorial < Chapter


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
    '''A tutorial, large or small'''
    class Meta:
        verbose_name = 'Tutoriel'
        verbose_name_plural = 'Tutoriels'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)
    authors = models.ManyToManyField(User, verbose_name='Auteurs')

    icon = models.ImageField(upload_to=tutorial_icon_path,
                             null=True, blank=True)

    # We could distinguish large/small tutorials by looking at what chapters
    # are contained directly in a tutorial, but that'd be more complicated than a field
    is_mini = models.BooleanField('Est un mini-tutoriel')
    is_visible = models.BooleanField('Est visible publiquement')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/tutoriels/voir/%s-%s/' % (self.pk, slugify(self.title))

    def get_parts(self):
        return Part.objects.all()\
            .filter(tutorial__pk=self.pk)\
            .order_by('position_in_tutorial')


def get_last_tutorials():
    # TODO: Sort by publish date (or update?)
    return Tutorial.objects.all().filter(is_visible=True).order_by('title')[:3]

    def get_chapter(self):
        '''Gets the chapter associated with the tutorial if it's small'''
        # We can use get since we know there'll only be one chapter
        return Chapter.objects.get(tutorial__pk=self.pk)


class Part(models.Model):
    '''A part, containing chapters'''
    class Meta:
        verbose_name = 'Partie'
        verbose_name_plural = 'Parties'

    # A part has to belong to a tutorial, since only tutorials with parts
    # are large tutorials
    tutorial = models.ForeignKey(Tutorial, verbose_name='Tutoriel parent')
    position_in_tutorial = models.IntegerField('Position dans le tutoriel')

    title = models.CharField('Titre', max_length=80)

    introduction = models.TextField('Introduction')
    conclusion = models.TextField('Conclusion')

    # The list of chapters is shown between introduction and conclusion

    def __unicode__(self):
        return '<Partie pour %s, %s>' % \
            (self.tutorial.title, self.position_in_tutorial)

    def get_absolute_url(self):
        return self.tutorial.get_absolute_url() + '%s-%s/' % (
            self.position_in_tutorial,
            slugify(self.title)
        )

    def get_chapters(self):
        return Chapter.objects.all()\
            .filter(part=self).order_by('position_in_part')


class Chapter(models.Model):
    '''A chapter, containing text'''
    class Meta:
        verbose_name = 'Chapitre'
        verbose_name_plural = 'Chapitres'

    # A chapter may belong to a part, that's where the difference between large
    # and small tutorials is.
    part = models.ForeignKey(Part, null=True, blank=True,
                             verbose_name='Partie parente')

    position_in_part = models.IntegerField('Position dans la partie',
                                           null=True, blank=True)

    # If the chapter doesn't belong to a part, it's a small tutorial; we need
    # to bind informations about said tutorial directly
    tutorial = models.ForeignKey(Tutorial, null=True, blank=True,
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
        if self.tutorial:
            return self.tutorial.get_absolute_url()

        elif self.part:
            return self.part.get_absolute_url() + '%s-%s' % (
                self.position_in_part,
                slugify(self.title)
            )

        else:
            return '/tutoriels/'

    def get_extract_count(self):
        return Extract.objects.all().filter(chapter__pk=self.pk).count()

    def get_extracts(self):
        return Extract.objects.all()\
            .filter(chapter__pk=self.pk)\
            .order_by('position_in_chapter')

    def get_tutorial(self):
        if self.part:
            return self.part.tutorial
        return self.tutorial


class Extract(models.Model):
    '''A content extract from a chapter'''
    class Meta:
        verbose_name = 'Extrait'
        verbose_name_plural = 'Extraits'

    title = models.CharField('Titre', max_length=80)
    chapter = models.ForeignKey(Chapter, verbose_name='Chapitre parent')
    position_in_chapter = models.IntegerField('Position dans le chapitre')
    text = models.TextField('Texte')

    def get_absolute_url(self):
        return '%s#%s-%s' % (
            self.chapter.get_absolute_url(),
            self.position_in_chapter,
            slugify(self.title)
        )
