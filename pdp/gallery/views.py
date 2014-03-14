# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from datetime import datetime

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST

from pdp.utils import render_template, slugify
from pdp.gallery.models import UserGallery, Image, Gallery
from pdp.gallery.forms import ImageForm, EditImageForm, GalleryForm, \
    UserGalleryForm


@login_required
def gallery_list(request):
    """Display the gallery list with all their images.

    Returns:
        HttpResponse

    """
    galleries = UserGallery.objects.all().filter(user=request.user)

    return render_template('gallery/gallery_list.html', {
        'galleries': galleries
    })


@login_required
def gallery_details(request, gal_pk, gal_slug):
    """Display a gallery.

    Returns:
        HttpResponse

    """

    gal = get_object_or_404(Gallery, pk=gal_pk)
    gal_mode = get_object_or_404(UserGallery, gallery=gal, user=request.user)
    images = gal.get_images()

    return render_template('gallery/gallery_details.html', {
        'gallery': gal,
        'gallery_mode': gal_mode,
        'images': images
    })


@login_required
def new_gallery(request):
    """Create a new gallery.

    Returns:
        HttpResponse

    """
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
        form = GalleryForm()

    return render_template('gallery/new_gallery.html', {
        'form': form
    })


@require_POST
@login_required
def modify_gallery(request):
    """Modify a gallery.

    Returns:
        HttpResponse

    """
    # Global actions

    if 'delete_multi' in request.POST:
        l = request.POST.getlist('items')

        perms = UserGallery.objects\
            .filter(gallery__pk__in=l, user=request.user, mode='W')\
            .count()

        # Check that the user has the RW right on each gallery
        if perms < len(l):
            raise PermissionDenied

        # Delete all the permissions on all the selected galleries
        UserGallery.objects.filter(gallery__pk__in=l).delete()
        # Delete all the images of the gallery (autodelete of file)
        Image.objects.filter(gallery__pk__in=l).delete()
        # Finally delete the selected galleries
        Gallery.objects.filter(pk__in=l).delete()

        return redirect(reverse('pdp.gallery.views.gallery_list'))

    # Gallery-specific actions

    try:
        gal_pk = request.POST['gallery']
    except KeyError:
        raise Http404

    gal = get_object_or_404(Gallery, pk=gal_pk)
    gal_mode = get_object_or_404(UserGallery, gallery=gal, user=request.user)

    # Disallow actions to read-only members
    if gal_mode.mode != 'W':
        raise PermissionDenied

    if 'adduser' in request.POST:
        form = UserGalleryForm(request.POST)
        u = get_object_or_404(User, username=request.POST['user'])

        # If the user already owns the gallery, we don't add him again
        if UserGallery.objects.filter(gallery=gal, user=u).count() > 0:
            raise PermissionDenied

        if form.is_valid():
            ug = UserGallery()
            ug.user = u
            ug.gallery = gal
            ug.mode = 'W'
            ug.save()

    return redirect(gal.get_absolute_url())


@require_POST
@login_required
def del_image(request, gal_pk):
    """Remove an image from a gallery.

    Returns:
        HttpResponse

    """
    gal = get_object_or_404(Gallery, pk=gal_pk)
    gal_mode = get_object_or_404(UserGallery, gallery=gal, user=request.user)

    if gal_mode.mode != 'W':
        raise PermissionDenied

    liste = request.POST.getlist('items')
    Image.objects.filter(pk__in=liste).delete()

    return redirect(gal.get_absolute_url())


@login_required
def edit_image(request, gal_pk, img_pk):
    """Edit an image.

    Returns:
        HttpResponse

    """
    gal = get_object_or_404(Gallery, pk=gal_pk)
    img = get_object_or_404(Image, pk=img_pk)

    if request.method == 'POST':
        form = EditImageForm(request.POST)
        if form.is_valid():
            img.title = request.POST['title']
            img.legend = request.POST['legend']
            img.update = datetime.now()

            img.save()

            # Redirect to the document list after POST
            return redirect(gal.get_absolute_url())
    else:
        form = EditImageForm(initial={
            'title': img.title,
            'legend': img.legend})

    return render_template('gallery/edit_image.html', {
        'form': form,
        'gallery': gal,
        'image': img
    })


@require_POST
@login_required
def modify_image(request):
    """Modify an image.

    Returns:
        HttpResponse

    """
    # We only handle secured POST actions
    try:
        gal_pk = request.POST['gallery']
    except KeyError:
        raise Http404

    gal = get_object_or_404(Gallery, pk=gal_pk)
    gal_mode = get_object_or_404(UserGallery, gallery=gal, user=request.user)

    # Only allow RW users to modify images
    if gal_mode.mode != 'W':
        raise PermissionDenied

    if 'delete' in request.POST:
        img = get_object_or_404(Image, pk=request.POST['image'])
        img.delete()

    elif 'delete_multi' in request.POST:
        l = request.POST.getlist('items')
        Image.objects.filter(pk__in=l).delete()

    return redirect(gal.get_absolute_url())


@login_required
def new_image(request, gal_pk):
    """Add a new image to a gallery.

    Returns:
        HttpResponse

    """
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
        form = ImageForm()  # A empty, unbound form

    return render_template('gallery/new_image.html', {
        'form': form,
        'gallery': gal
    })
