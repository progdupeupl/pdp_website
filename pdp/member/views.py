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

"""Member app's views."""

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.views.decorators.debug import sensitive_post_parameters

from pdp.utils import render_template
from pdp.utils.tokens import generate_token
from pdp.utils.paginator import paginator_range
from pdp.article.models import Article
from pdp.tutorial.models import Tutorial

from pdp.member.models import Profile
from pdp.member.forms import LoginForm, ProfileForm, RegisterForm, \
    ChangePasswordForm


def index(request):
    """Display list of registered users.

    Returns:
        HttpResponse

    """
    members = User.objects.order_by('-date_joined')

    paginator = Paginator(members, settings.MEMBERS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_members = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_members = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_members = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render_template('member/index.html', {
        'members': shown_members,
        'members_count': members.count(),
        'pages': paginator_range(page, paginator.num_pages),
        'nb': page,
    })


@login_required
def actions(request):
    """Show avaible actions for current user, like a customized homepage.

    This may be very temporary.

    Returns:
        HttpResponse

    """

    # TODO: Seriously improve this page, and see if cannot be merged in
    #       pdp.pages.views.home since it will be more coherent to give an
    #       enhanced homepage for registered users

    return render_template('member/actions.html')


def details(request, user_name):
    """Display details about a profile.

    Returns:
        HttpResponse

    """
    usr = get_object_or_404(User, username=user_name)
    profile = get_object_or_404(Profile, user=usr)

    return render_template('member/profile.html', {
        'usr': usr, 'profile': profile
    })


@login_required
def edit_profile(request):
    """Edit an user's profile.

    Returns:
        HttpResponse

    """
    try:
        profile_pk = int(request.GET['profil'])
        profile = get_object_or_404(Profile, pk=profile_pk)
    except KeyError:
        profile = get_object_or_404(Profile, user=request.user)

    # Making sure the user is allowed to do that
    if not request.user == profile.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.data
            profile.biography = data['biography']
            profile.site = data['site']
            profile.user.email = data['email']
            profile.show_email = 'show_email' in data

            # Save the user and it's associated profile
            profile.user.save()
            profile.save()
            return redirect(profile.get_absolute_url())
        else:
            raise Http404
    else:
        return render_template('member/edit_profile.html', {
            'profile': profile
        })


@sensitive_post_parameters('password')
def login_view(request):
    """Allow users to log into their accounts.

    Returns:
        HttpResponse

    """
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['get_token'] = generate_token()
                if not 'remember' in request.POST:
                    request.session.set_expiry(0)
                return redirect(reverse('pdp.pages.views.home'))
            else:
                error = u'Les identifiants fournis ne sont pas valides'
        else:
            error = (u'Veuillez spécifier votre identifiant '
                     u'et votre mot de passe')
    else:
        form = LoginForm()
    csrf_tk['error'] = error
    csrf_tk['form'] = form

    return render_template('member/login.html', csrf_tk)


@login_required
def logout_view(request):
    """Allow users to log out of their accounts.

    Returns:
        HttpResponse

    """
    # If we got a secure POST, we disconnect
    if request.method == 'POST':
        logout(request)
        request.session.clear()
        return redirect(reverse('pdp.pages.views.home'))

    # Elsewise we ask the user to submit a form with correct csrf token
    return render_template('member/logout.html')


@sensitive_post_parameters('password', 'password_confirm')
def register_view(request):
    """Allow new users to register, creating them an account.

    Returns:
        HttpResponse

    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])
            profile = Profile(user=user, show_email=False)
            profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render_template('member/register_success.html')
        else:
            return render_template('member/register.html', {'form': form})

    form = RegisterForm()
    return render_template('member/register.html', {
        'form': form
    })


# Settings for public profile

@login_required
def settings_profile(request):
    """Set current user's profile settings.

    Returns:
        HttpResponse

    """
    # extra information about the current user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            profile.biography = form.data['biography']
            profile.site = form.data['site']
            profile.show_email = 'show_email' in form.data
            profile.avatar_url = form.data['avatar_url']
            profile.save()

            messages.success(request,
                             u'Le profil a correctement été mis à jour.')

            return redirect('/membres/parametres/profil')
        else:
            return render_template('member/settings_profile.html', c)
    else:
        form = ProfileForm(request.user, initial={
            'biography': profile.biography,
            'site': profile.site,
            'avatar_url': profile.avatar_url,
            'show_email': profile.show_email}
        )
        c = {
            'form': form
        }
        return render_template('member/settings_profile.html', c)


@login_required
def settings_account(request):
    """Set current user's account settings.

    Returns:
        HttpResponse

    """
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        c = {
            'form': form,
        }
        if form.is_valid():
            request.user.set_password(form.data['password_new'])
            request.user.save()

            messages.success(request, u'Le mot de passe a bien été modifié.')
            return redirect('/membres/parametres/profil')

        else:
            return render_template('member/settings_account.html', c)
    else:
        form = ChangePasswordForm(request.user)
        c = {
            'form': form,
        }
        return render_template('member/settings_account.html', c)


@login_required
def publications(request):
    """Show current user's articles and tutorials.

    Returns:
        HttpResponse

    """

    user_articles = Article.objects.filter(
        author=request.user).order_by('-pubdate')
    user_tutorials = Tutorial.objects.filter(
        authors=request.user).order_by('-pubdate')

    c = {
        'user_articles': user_articles,
        'user_tutorials': user_tutorials,
    }

    return render_template('member/publications.html', c)
