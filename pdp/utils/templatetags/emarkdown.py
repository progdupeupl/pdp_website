# coding: utf-8


import cssstyles
import markdown
from django import template
from django.utils.safestring import mark_safe

md_cssstyle = cssstyles.StyleExtension()

register = template.Library()

@register.filter(needs_autoescape=False)
def emarkdown(value):
	# TODO: use simple quotes and 4-spaces tabulations like in other files

	return mark_safe(markdown.markdown(value, extensions=[md_cssstyle,"codehilite(force_linenos=True)","extra"], safe_mode=True))
