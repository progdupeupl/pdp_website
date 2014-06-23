// Remplacez la valeur UA-XXXXXX-Y par l'identifiant analytics de votre site.
gaProperty = '{{ key }}'

// Désactive le tracking si le cookie d’Opt-out existe déjà.
var disableStr = 'ga-disable-' + gaProperty;

if (document.cookie.indexOf('hasConsent=false') > -1) {
    window[disableStr] = true;
}

// Cette fonction retourne la date d’expiration du cookie de consentement 
function getCookieExpireDate() { 
    var cookieTimeout = 34214400000;// Le nombre de millisecondes que font 13 mois
    var date = new Date();
    date.setTime(date.getTime()+cookieTimeout);
    var expires = "; expires="+date.toGMTString();
    return expires;
}

// Cette fonction est appelée pour afficher la demande de consentement
function askConsent(){
    var bodytag = document.getElementsByTagName('header')[0];
    var div = document.createElement('div');
    div.setAttribute('id','cookie-banner');
    // Le code HTML de la demande de consentement
    // Vous pouvez modifier le contenu ainsi que le style
    div.innerHTML =  '<p>Ce site utilise Google Analytics.\
    En continuant à naviguer, vous nous autorisez à déposer des cookies à des fins de \
    mesure d’audience. \
    <a href="javascript:gaOptout()" class="button mini">Non merci</a> \
    </p>';
    bodytag.insertBefore(div,bodytag.firstChild); // Ajoute la bannière juste au début de la page 
    document.getElementsByTagName('body')[0].className+=' cookiebanner';
}

// Retourne la chaine de caractère correspondant à nom=valeur
function getCookie(NomDuCookie)  {
    if (document.cookie.length > 0) {
        begin = document.cookie.indexOf(NomDuCookie+"=");
        if (begin != -1)  {
            begin += NomDuCookie.length+1;
            end = document.cookie.indexOf(";", begin);
            if (end == -1) end = document.cookie.length;
            return unescape(document.cookie.substring(begin, end)); 
        }
     }
    return null;
}

// Fonction d'effacement des cookies   
function delCookie(name )   {
    path = ";path=" + "/";
    domain = ";domain=" + "."+document.location.hostname;
    var expiration = "Thu, 01-Jan-1970 00:00:01 GMT";
    document.cookie = name + "=" + path + domain + ";expires=" + expiration;
}

// Efface tous les types de cookies utilisés par Google Analytics
function deleteAnalyticsCookies() {
    var cookieNames = ["__utma","__utmb","__utmc","__utmz","_ga"]
    for (var i=0; i<cookieNames.length; i++)
        delCookie(cookieNames[i])
}

// La fonction d'opt-out
function gaOptout() {
    document.cookie = disableStr + '=true;'+ getCookieExpireDate() +' ; path=/';
    document.cookie = 'hasConsent=false;'+ getCookieExpireDate() +' ; path=/';

    var div = document.getElementById('cookie-banner');

    if ( div!= null ) div.innerHTML = '<p> Vous vous êtes opposé \
    Au dépôt de cookies de mesures d\'audience dans votre navigateur.</p>'

    window[disableStr] = true;
    deleteAnalyticsCookies();
}

// Ce bout de code vérifie que le consentement n'a pas déjà été obtenu avant d'afficher
// la baniére
var consentCookie =  getCookie('hasConsent');
if (!consentCookie) {
 //L'utilisateur n'a pas encore de cookie de consentement
 var referrer_host = document.referrer.split('/')[2]; 
   if ( referrer_host != document.location.hostname ) {
     // si il vient d'un autre site on désactive le tracking et on affiche la
     // demande de consentement
     window[disableStr] = true;
     window[disableStr] = true;
     window.onload = askConsent;
   } else { //sinon on lui dépose un cookie 
      document.cookie = 'hasConsent=true; '+ getCookieExpireDate() +' ; path=/'; 
   }
}

// Il vous reste à insérer votre tag javascript ici   
