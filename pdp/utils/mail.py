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

"""Module containing some functions to send mails."""

from django.template.loader import render_to_string
from django.core.mail import send_mail


def send_templated_mail(subject, template, context, recipients):
    """Send an email based on a template.

    Args:
        subject: (string) Subject of the email
        template: (string) Name of the template used for the message
        context: (dictionary) Dictionary used for the message
        recipients: (list) List of the recipients

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    message = render_to_string('mail/' + template, context)

    return send_mail(
        subject=subject,
        message=message,
        from_email='Chtaline <chtaline@progdupeu.pl>',
        recipient_list=recipients
    )


def send_mail_to_confirm_registration(token):
    """Send an email to confirm registration.

    Args:
        token: (ActivationToken) token to be send

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    return send_templated_mail(
        subject=u"Confirmation d’inscription à Progdupeupl",
        template=u'confirm_registration.txt',
        context={
            'user': token.user,
            'link': token.token
        },
        recipients=[token.user.email]
    )
