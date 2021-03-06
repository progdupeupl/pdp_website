# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

"""Member app's views."""

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404, HttpResponse
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

from django.db import transaction

from pdp.utils import render_template, bot
from pdp.utils.tokens import generate_token
from pdp.utils.paginator import paginator_range
from pdp.utils.mail import send_mail_to_confirm_registration, \
    send_mail_to_confirm_password_reset, send_mail_temporary_password

from pdp.tutorial.models import Tutorial

from pdp.member.models import Profile, ActivationToken, ForgotPasswordToken, \
    create_activation_token, create_forgot_password_token, \
    generate_user_password

from pdp.member.forms import LoginForm, ProfileForm, RegisterForm, \
    ChangePasswordForm, LostPasswordForm


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


@login_required(redirect_field_name='suivant')
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


@login_required(redirect_field_name='suivant')
@transaction.atomic
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

    If the `suivant` HTTP GET field is given, then this view will redirect the
    user to the given URL after successful auth.

    Returns:
        HttpResponse

    """
    csrf_tk = {}
    csrf_tk.update(csrf(request))

    if 'suivant' in request.GET:
        csrf_tk['next'] = request.GET['suivant']

    error = False
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    # Yeah auth successful
                    login(request, user)
                    request.session['get_token'] = generate_token()

                    # Avoid persistant session if asked to do so
                    if 'remember' not in request.POST:
                        request.session.set_expiry(0)

                    # Redirect if connected was required from another page
                    if 'suivant' in request.GET:
                        return redirect(request.GET['suivant'])

                    # Elsewise redirect to home
                    return redirect(reverse('pdp.pages.views.home'))

                else:
                    # User is not active, check if user was banned or if he
                    # did not validate his account yet.

                    try:
                        activation = ActivationToken.objects.get(user=user)
                    except ActivationToken.DoesNotExist:
                        activation = None

                    if activation is None:
                        error = 'Ce compte est désactivé.'
                    else:
                        # TODO: resend key link
                        error = 'Ce compte n’a pas encore été activé.'
            else:
                error = u'Les identifiants fournis ne sont pas valides.'
        else:
            error = (u'Veuillez spécifier votre identifiant '
                     u'et votre mot de passe.')
    else:
        form = LoginForm()

    csrf_tk['error'] = error
    csrf_tk['form'] = form

    return render_template('member/login.html', csrf_tk)


@login_required(redirect_field_name='suivant')
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


def password_reset_view(request):
    """Allow users to recover their account when they lost their passwords.

    Returns:
        HttpResponse

    """
    error = None
    if request.method == 'POST':
        form = LostPasswordForm(request.POST)

        if form.is_valid():
            data = form.data

            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                user = None

            if user is not None:
                token = create_forgot_password_token(user)
                send_mail_to_confirm_password_reset(token)

                return render_template('member/password_reset_confirm.html')

            else:
                error = 'Utilisateur introuvable avec cette adresse.'
    else:
        form = LostPasswordForm()

    return render_template('member/password_reset.html', {
        'form': form, 'error': error
    })


def confirm_password_reset_view(request, token):
    if not request.user.is_authenticated():
        token = get_object_or_404(ForgotPasswordToken, token=token)

        if token.is_valid():

            # Login the user
            user = token.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            # Set a new temporary password and send it to the user
            password = generate_user_password()

            user.set_password(password)
            user.save()

            send_mail_temporary_password(user, password)

            # Delete the ForgotPasswordToken object
            token.delete()

            messages.success(
                request,
                'Votre mot de passe temporaire vous a été envoyé par mail. '
                'Utilisez-le dès maintenant pour le changer par un nouveau '
                'mot de passe.'
            )

            return redirect(reverse('pdp.member.views.settings_account'))
        else:
            return HttpResponse('Token expiré')
    else:
        raise PermissionDenied


@sensitive_post_parameters('password', 'password_confirm')
@transaction.atomic
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
                data['password']
            )

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.is_active = False
            user.save()

            profile = Profile(
                user=user,
                show_email=False,
            )

            profile.save()

            # We generate a new activation key for the user and save it
            token = create_activation_token(user)

            send_mail_to_confirm_registration(token)

            return render_template('member/register_confirmation.html')
        else:
            return render_template('member/register.html', {'form': form})

    form = RegisterForm()
    return render_template('member/register.html', {
        'form': form
    })


def confirm_registration_view(request, token):
    """Confirm user's registration.

    Returns:
        HttpResponse

    """
    if not request.user.is_authenticated():
        token = get_object_or_404(ActivationToken, token=token)

        # Check if the activation key is still valid
        if token.is_valid():

            # Activate the user account
            user = token.user
            user.is_active = True
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            user.save()

            # Delete the ActivationToken object
            token.delete()

            # Login the user and congrats him

            login(request, user)

            messages.success(
                request,
                u'Votre compte est maintenant activé !'
            )

            if settings.BOT_ENABLED:
                bot.send_welcome_private_message(user)

            return redirect(reverse('pdp.pages.views.home'))
        else:
            return HttpResponse('token expiré')
    else:
        raise Http404


# Settings for public profile

@login_required(redirect_field_name='suivant')
def settings_profile(request):
    """Set current user's profile settings.

    Returns:
        HttpResponse

    """

    # Extra information about the current user
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        form = ProfileForm(request.user, request.POST)

        if form.is_valid():
            profile.biography = form.data['biography']
            profile.site = form.data['site']
            profile.show_email = 'show_email' in form.data
            profile.avatar_url = form.data['avatar_url']
            profile.mail_on_private_message = \
                'mail_on_private_message' in form.data
            profile.save()

            messages.success(
                request, u'Le profil a correctement été mis à jour.')

            return redirect('/membres/parametres/profil')

        else:
            return render_template('member/settings_profile.html', {
                'form': form
            })
    else:
        form = ProfileForm(request.user, initial={
            'biography': profile.biography,
            'site': profile.site,
            'avatar_url': profile.avatar_url,
            'show_email': profile.show_email,
            'mail_on_private_message': profile.mail_on_private_message}
        )

        return render_template('member/settings_profile.html', {
            'form': form
        })


@login_required(redirect_field_name='suivant')
def settings_account(request):
    """Set current user's account settings.

    Returns:
        HttpResponse

    """

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            request.user.set_password(form.data['password_new'])
            request.user.save()

            messages.success(request, u'Le mot de passe a bien été modifié.')
            return redirect('/membres/parametres/profil')

        else:
            return render_template('member/settings_account.html', {
                'form': form
            })
    else:
        form = ChangePasswordForm(request.user)

        return render_template('member/settings_account.html', {
            'form': form
        })


@login_required(redirect_field_name='suivant')
def publications(request):
    """Show current user's tutorials.

    Returns:
        HttpResponse

    """

    tutorials = Tutorial.objects \
        .filter(authors=request.user)

    # Handle filter, if any
    active_filter = 'all'
    if 'filtre' in request.GET:
        if request.GET['filtre'] == 'beta':
            active_filter = 'beta'
            tutorials = tutorials.filter(is_beta=True)
        elif request.GET['filtre'] == 'publie':
            tutorials = tutorials.filter(is_visible=True)
            active_filter = 'published'

    # Finally order by pubdate
    tutorials = tutorials.order_by('-pubdate')

    return render_template('member/publications.html', {
        'user_tutorials': tutorials,
        'active_filter': active_filter
    })
