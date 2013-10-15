# -*- coding: utf-8 -*-

# The max size in bytes

from django.conf import settings
from datetime import datetime
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from pdp.utils import render_template, slugify
from pdp.gallery.models import UserGallery, Image, Gallery
from pdp.gallery.forms import ImageForm, GalleryForm, UserGalleryForm


@login_required
def gallery_list(request):
    '''
    Display the gallery list with all their images
    '''
    galleries = UserGallery.objects.all().filter(user=request.user)

    return render_template('gallery/gallery_list.html', {
        'galleries': galleries
    })


@login_required
def gallery_details(request, gal_pk, gal_slug):
    '''
    Gallery details
    '''

    gal = get_object_or_404(Gallery, pk=gal_pk)
    images = gal.get_images()

    return render_template('gallery/gallery_details.html', {
        'gallerie': gal,
        'images': images
    })


@login_required
def new_gallery(request):
    '''
    Creates a new gallery
    '''
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            data = form.data
            # Creating the gallery
            gal = Gallery()
            gal.title = data['title']
            gal.subtitle = data['subtitle']
            gal.slug = slugify(data['title'])
            gal.pubdate = datetime.now()
            gal.save()

            # Attach user
            userg = UserGallery()
            userg.gallery = gal
            userg.mode = 'W'
            userg.user = request.user
            userg.save()

            return redirect(gal.get_absolute_url())

        else:
            # TODO: add errors to the form and return it
            raise Http404
    else:
        form = GalleryForm()
        return render_template('gallery/new_gallery.html', {
            'form': form
        })


@login_required
def share_gallery(request, gal_pk):
    '''
    Share gallery with users
    '''
    gal = get_object_or_404(Gallery, pk=gal_pk)
    if request.method == 'POST':
        u = get_object_or_404(User, username=request.POST['user'])
        form = UserGalleryForm(request.POST)
        if form.is_valid():
            ug = UserGallery()
            ug.user = u
            ug.gallery = gal
            ug.mode = request.POST['mode']

            ug.save()

            # Redirect to the document list after POST
            return redirect(gal.get_absolute_url())
        else:
            # TODO: add errors to the form and return it
            raise Http404
    else:
        form = UserGalleryForm()  # A empty, unbound form
        return render_template('gallery/share_gallery.html', {
            'form': form,
            'gallerie': gal
        })


@login_required
def del_gallery(request):
    if request.method == 'POST':
        liste = request.POST.getlist('items')
        for i in liste:
            del_image(request, i)
        UserGallery.objects.filter(gallery__pk__in=liste).delete()
        Gallery.objects.filter(pk__in=liste).delete()
    return gallery_list(request)


@login_required
def del_image(request, gal_pk):

    gal = get_object_or_404(Gallery, pk=gal_pk)
    if request.method == 'POST':
        liste = request.POST.getlist('items')
        Image.objects.filter(pk__in=liste).delete()
        return redirect(gal.get_absolute_url())
    return redirect(gal.get_absolute_url())


@login_required
def edit_image(request, gal_pk, img_pk):
    '''
    Creates a new image
    '''
    gal = get_object_or_404(Gallery, pk=gal_pk)
    img = get_object_or_404(Image, pk=img_pk)

    if request.method == 'POST':
        form = ImageForm(request.POST)
        if form.is_valid():
            img.title = request.POST['title']
            img.legend = request.POST['legend']
            img.update = datetime.now()

            img.save()

            # Redirect to the document list after POST
            return redirect(gal.get_absolute_url())
        else:
            # TODO: add errors to the form and return it
            raise Http404
    else:
        form = ImageForm()  # A empty, unbound form
        return render_template('gallery/edit_image.html', {
            'form': form,
            'gallerie': gal,
            'image': img
        })


@login_required
def new_image(request, gal_pk):
    '''
    Creates a new image
    '''
    gal = get_object_or_404(Gallery, pk=gal_pk)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() \
           and request.FILES['physical'].size < settings.IMAGE_MAX_SIZE:
            img = Image()
            img.physical = request.FILES['physical']
            img.gallery = gal
            img.title = request.POST['title']
            img.slug = slugify(request.FILES['physical'])
            img.legend = request.POST['legend']
            img.pubdate = datetime.now()

            img.save()

            # Redirect to the document list after POST
            return redirect(gal.get_absolute_url())
        else:
            # TODO: add errors to the form and return it
            raise Http404
    else:
        form = ImageForm()  # A empty, unbound form
        return render_template('gallery/new_image.html', {
            'form': form,
            'gallerie': gal
        })
