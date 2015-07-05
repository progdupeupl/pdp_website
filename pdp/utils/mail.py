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


def render_email_template(template, context):
    """Render an email body based on a template.

    Args:
        template: (string) Name of the template user for the message
        context: (dictionary) Rendering context of the template

    Returns:
        String containing the rendered email body.

    """
    return render_to_string('mail/{}'.format(template), context)


def send_templated_mail(subject, template, context, recipients):
    """Send an email based on a template.

    Args:
        subject: (string) Subject of the email
        template: (string) Name of the template used for the message
        context: (dictionary) Rendering context of the template
        recipients: (list) List of the recipients

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    message = render_email_template(template, context)

    return send_mail(
        subject="[PDP] {}".format(subject),
        message=message,
        from_email='Chtaline <chtaline@progdupeupl.org>',
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


def send_mail_to_confirm_password_reset(token):
    """Send an email to confirm password reset.

    Args:
        token: (ForgotPasswordToken) token to be send

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    return send_templated_mail(
        subject=u"Confirmation de réinitialisation de mot de passe",
        template=u'confirm_password_reset.txt',
        context={
            'user': token.user,
            'link': token.token
        },
        recipients=[token.user.email]
    )


def send_mail_temporary_password(user, password):
    """Send an email with a new temporary password.

    Args:
        user: the user we just changed the password
        password: the new user password

    Returns:
        Number of successfully delivered messages (0 or 1)

    """

    return send_templated_mail(
        subject=u"Réinitialisation de mot de passe",
        template=u'password_reset.txt',
        context={
            'user': user,
            'password': password
        },
        recipients=[user.email]
    )


def send_mail_new_private_message(topic, user):
    return send_templated_mail(
        subject='Nouveau message privé de {}'.format(topic.author.username),
        template='new_private_message.txt',
        context={
            'topic': topic
        },
        recipients=[user.email]
    )
