# coding: utf-8

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404

from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.core.context_processors import csrf

from pdp.utils.tokens import generate_token
from pdp.utils import render_template

from models import Profile
from forms import LoginForm, ProfileForm, RegisterForm


def index(request):
    '''Affiche la liste des profils des membres inscrits'''
    p = Profile.objects.all()

    return render_template('member/index.html', {
        'profiles': p
    })


def details(request, user_name):
    '''Affiche les détails concernant un profil particulier'''
    u = get_object_or_404(User, username=user_name)

    try:
        p = u.get_profile()
    except SiteProfileNotAvailable:
        raise Http404

    return render_template('member/profile.html', {
        'usr': u, 'profile': p
    })


@login_required
def edit_profile(request):
    try:
        profile_pk = int(request.GET['profil'])
    except KeyError:
        raise Http404

    p = get_object_or_404(Profile, pk=profile_pk)

    # On vérifie que l'utilisateur a bien le droit de faire ça
    if not request.user == p.user:
        raise Http404

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            data = form.data

            p.biography = data['biography']
            p.site = data['site']
            p.show_email = 'show_email' in data
            p.save()

            return redirect(p.get_absolute_url())

        else:
            raise Http404

    else:
        return render_template('member/edit_profile.html', {
            'profile': p
        })


def login_view(request):
    c = {}
    c.update(csrf(request))

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
                return redirect('/')
            else:
                error = 'Ce compte n\'est pas actif'
        else:
            error = 'Le couple pseudo/mot de passe est erroné'
    else:
        form = LoginForm()

    c['error'] = error
    c['form'] = form

    return render_template('member/login.html', c)


@login_required
def logout_view(request):
    logout(request)
    request.session.clear()
    return redirect('/')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'])

            profile = Profile(user=user, show_email='show_email' in data)
            profile.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return render_template('member/register_success.html')

    return render_template('member/register.html')