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

from pdp.forum.models import Forum

def index(request):
    '''Displays the list of registered users'''
    members = User.objects.order_by('date_joined')
    return render_template('member/index.html', {
        'members': members
    })


def details(request, user_name):
    '''Displays details about a profile'''
    usr = get_object_or_404(User, username=user_name)
    
    try:
        profile = usr.get_profile()
    except SiteProfileNotAvailable:
        raise Http404
    
    forums = Forum.objects.all()
    
    return render_template('member/profile.html', {
        'usr': usr, 'profile': profile, 'forums': forums
    })


@login_required
def edit_profile(request):
    try:
        profile_pk = int(request.GET['profil'])
        profile = get_object_or_404(Profile, pk=profile_pk)
    except KeyError:
        profile = get_object_or_404(Profile, user=request.user)
        
    # Making sure the user is allowed to do that
    if not request.user == profile.user:
        raise Http404
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


def login_view(request):
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
                return redirect('/')
            else:
                error = 'Les identifiants fournis ne sont pas valides'
        else:
            error = 'Veuillez spécifier votre identifiant et votre mot de passe'
    else:
        form = LoginForm()
    csrf_tk['error'] = error
    csrf_tk['form'] = form
    return render_template('member/login.html', csrf_tk)


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
