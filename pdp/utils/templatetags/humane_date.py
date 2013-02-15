# coding: utf-8

# Ce fichier provient en intégralité de Progmod ; quelques parties ont
# étées modifiées cependant pour que ça puisse fonctionner sur pdp
# Merci à eux !

from datetime import *
from django import template
from pytz import timezone, UnknownTimeZoneError
import pdp.settings


def humane_date(date, conf={}):
    """Exprime la date d'un événement d'une façon agréable à lire pour un humain.

    Compare la date à afficher au moment actuel :
    - il y a 3 minutes et 25 secondes
    - il y a 2 heures
    - hier à 18 heures
    - il y a trois mois

    Arguments:
    - date : un 'datetime', avec éventuellement une information de
      fuseau horaire (timezone)

    - conf : un dictionnaire contenant les éventuels paramètres
      optionnels de la fonction. On utilise un dictionnaire plutôt que
      plusieurs arguments car la fonction est destinée à être utilisée
      comme filtre Django, qui n'acceptent qu'un seul paramètre
      supplémentaire. Les valeurs actuellement supportées sont les
      suivantes :
      - 'debug':False : si True, ajoute des informations de debug
      - 'precise':False : si True, affiche toujours la date sans limite de précision
      - 'precision_limit':3 : limite de précision par défaut
      - 'disable':False : si True, affiche la date de façon habituelle
      - 'full_after_week':True : si True, affiche la date complète au delà d'une semaine

    Implémentation : on repère les deux unités significatives
    ((minutes, secondes) ou (mois, jours)) par exemple. Par défaut, on
    n'affiche la seconde que si la première est inférieure
    à 'precision_limit'. Si 'precise' est vraie, on affiche toujours
    la seconde.

    Il y a un cas particulier dans le cas où la date fournie contient
    un fuseau horaire : si les unités significatives sont (jours,
    heures) et que l'événement est distant d'au plus deux jours, ou
    bien se passe dans la même semaine, on renvoie une date absolue de
    la forme (H ∈ [0..23]) :
    - "hier à H heures" (distant de moins de deux jours : hier,
      avant-hier, demain, après-demain)
    - "mardi à H heures" (même semaine)
    Pour H = 0 et H = 12, on affiche plutôt 'minuit' et 'midi'


    """

    precise_limit = conf.get('precision_limit', 3)
    precise = conf.get('precise', False)
    debug = conf.get('debug', False)
    disable = conf.get('disable', False)
    full_after_week = conf.get('full_after_week', True)
    tz = date.tzinfo
    use_tz = (tz is not None)

    today = datetime.now(tz)
    diff = date - today

    def fulldate(date, today):
        if (date.year == today.year):
            return date.strftime("le %a %d %B à %H:%M:%S")
        else:
            return date.strftime("le %d/%m/%Y à %H:%M:%S")

    if disable:
        return fulldate(date, today)

    def week(date):
        """Numéro de la semaine"""
        year, week, weekday = date.isocalendar()
        return year, week

    secondes = ('seconde', abs(diff).seconds % 60)
    minutes = ('minute', abs(diff).seconds // 60 % 60)
    heures = ('heure', abs(diff).seconds // 60 // 60 % 24)
    jours = ('jour', abs(diff).days % 31)
    mois = ('mois', int(abs(diff).days % 365 // 30.5))
    annees = ('an', abs(diff).days // 365)

    if not debug:
        debug_msg = ' '
    else:
        debug_msg = "[debug(humane_date) today:%s date:%s conf:%s] " % \
            (today, date, conf)

    prefixe = "il y a" if date < today else "dans"

    def compte((str, n)):
        """Exprime l'unite demandée, avec un 's' au pluriel"""
        return "%d %s%s" % (n, str, 's' if n > 1 and str[-1] != 's' else '')

    def presente(unite1, unite2, prefixe=prefixe + ' '):
        """Exprime les deux unités fournies, en tenant compte de la précision souhaitée"""
        result = debug_msg + prefixe
        if (not precise and unite1[1] > precise_limit) or unite2[1] == 0:
            result += compte(unite1)
        elif unite1[1] == 0:
            result += compte(unite2)
        else:
            result += "%s et %s" % (compte(unite1), compte(unite2))
        return result

    daydiff = (date.date() - today.date()).days

    if abs(diff) < timedelta(seconds=1):
        return "maintenant"
    elif abs(diff) < timedelta(hours=1):
        return presente(minutes, secondes)
    elif daydiff == 0:
        return presente(heures, minutes)
    elif use_tz and (abs(daydiff) <= 2 or week(date) == week(today)):
        if abs(daydiff) <= 2:
            assert (date.day != today.day)
            jour = {-1: 'hier', -2: 'avant-hier', 1: 'demain',
                    2: 'après-demain'}[daydiff]
        elif week(date) == week(today):
            jour = {1: 'lundi', 2: 'mardi', 3: 'mercredi', 4: 'jeudi',
                    5: 'vendredi', 6: 'samedi', 7: 'dimanche'}[date.isoweekday()]
        heure = ('heure', date.hour)
        if not precise:
            heure_str = {0: 'minuit', 12: 'midi'}.get(heure[1], compte(heure))
        else:
            heure_str = presente(heure, ('minute', date.minute), prefixe='')
        return "%s%s à %s" % (debug_msg, jour, heure_str)
    elif use_tz and full_after_week:
        return fulldate(date, today)
    elif abs(diff) < timedelta(days=31):
        return presente(jours, heures)
    elif abs(diff) < timedelta(days=365):
        return presente(mois, jours)
    else:
        return presente(annees, mois)


def test(tz=None):
    """Tests pour la fonction humane_date"""
    def test_date(date, conf={}):
        pass
        #print "%s  : %s" % (date, humane_date(date, conf))
    #secondes

    def now(tz=None):
        return datetime.now(tz)

    test_date(now())
    test_date(now() - timedelta(seconds=2))
    test_date(now().replace(second=2))

    #minutes et secondes
    test_date(now() - timedelta(minutes=3))
    test_date(now() - timedelta(minutes=3, seconds=2))
    test_date(now().replace(minute=3, second=2))

    #heures et limite du jour
    def subtest(tz):
        test_date(now(tz) - timedelta(hours=1, minutes=2, seconds=5))
        test_date(
            now(tz) - timedelta(hours=3, minutes=12), {'precise': True})
        test_date(
            now(tz) - timedelta(hours=14, minutes=12), {'precise': True})
        test_date(now(tz) - timedelta(hours=23))
        test_date((now(tz) - timedelta(days=1)).replace(hour=0))
        test_date((now(tz) - timedelta(days=1)).replace(hour=12))
        test_date(now(tz) - timedelta(days=3))

    subtest(tz)

    # jours, mois, années
    test_date(now() - timedelta(days=45))
    test_date(now() - timedelta(days=130))
    test_date(now() - timedelta(days=365 + 20))
    test_date(now() - timedelta(days=365 + 92))
    test_date(now() - timedelta(days=5 * 365 + 25))

    #disable
    test_date(now(tz), {'disable': True})
    test_date(now(tz) - timedelta(days=1000), {'disable': True})

    #debug
    delta = timedelta(seconds=3, minutes=4, hours=5, days=6)
    test_date(now(tz) - delta, {'debug': True})


def do_humane_date(parser, token):
    content = token.split_contents()

    if not len(content) in (2, 3):
        raise template.SyntaxError, "Usage : {% humane_date variable (optional user timezone) %}"

    tz = "user_timezone"
    if len(content) == 3:
        tz = content[2]

    return HumaneDateNode(content[1], tz)


class HumaneDateNode(template.Node):
    def __init__(self, date_variable, tz_variable):
        self.date_variable = template.Variable(date_variable)
        self.tz_variable = template.Variable(tz_variable)

    def render(self, context):
        date = self.date_variable.resolve(context)
        tz = self.tz_variable.resolve(context)

        # On veut faire quoi maintenant ? convertir la date depuis la timezone
        # native vers la timezone de l'user, puis la donner à humane_date
        # régler le tzinfo ici depuis la config. bug si on utilise pas localize
        date_nn = timezone(pdp.settings.TIME_ZONE).localize(date)
        date_tz = date_nn.astimezone(tz)
        return humane_date(date_tz)


def set_timezone(request):
    tz = timezone(pdp.settings.TIME_ZONE)
    if request.user.is_authenticated():
        try:
            tz = timezone(request.user.get_profile().timezone)
        except UnknownTimeZoneError:
            pass

    return {'user_timezone': tz}

if __name__ == '__main__':
    # Test de la fonction 'humane_date'
    test(None)
    # On dépend de la bibliothèque 'pytz' pour fournir
    # un fuseau horaire
    test(timezone('Europe/Paris'))
else:
    # Enregistrement de 'humane_date' comme un filtre Django
    from django import template
    register = template.Library()
    register.filter('humane_date', humane_date)
    register.tag('humane_date', do_humane_date)
    humane_date.is_safe = True
