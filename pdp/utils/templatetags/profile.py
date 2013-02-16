# coding: utf-8

from django import template

from pdp.member.models import Profile

register = template.Library()


@register.filter('profile')
def profile(user):
    profile = Profile.objects.get(user=user)
    return profile
