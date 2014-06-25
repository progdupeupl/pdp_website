gaProperty = '{{ key }}'

var disableStr = 'ga-disable-' + gaProperty;

if (document.cookie.indexOf('hasConsent=false') > -1) {
    window[disableStr] = true;
}

function getCookieExpireDate() { 
    var cookieTimeout = 34214400000; // 13 months
    var date = new Date();
    date.setTime(date.getTime()+cookieTimeout);
    var expires = "; expires="+date.toGMTString();
    return expires;
}

function askConsent(){
    var bodytag = document.getElementsByTagName('header')[0];
    var div = document.createElement('div');
    div.setAttribute('id','cookie-banner');

    div.innerHTML =  '<p> \
    En continuant à naviguer, vous acceptez l’utilisation des cookies. \
    <a href="javascript:gaOk()" class="button mini success">Ok</a> \
    <a href="/pages/cgu#cookies" class="button mini">En savoir plus</a> \
    </p>';

    bodytag.insertBefore(div,bodytag.firstChild);
}

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

function delCookie(name )   {
    path = ";path=" + "/";
    domain = ";domain=" + "."+document.location.hostname;
    var expiration = "Thu, 01-Jan-1970 00:00:01 GMT";
    document.cookie = name + "=" + path + domain + ";expires=" + expiration;
}

function deleteAnalyticsCookies() {
    var cookieNames = ["__utma","__utmb","__utmc","__utmz","_ga"]
    for (var i=0; i<cookieNames.length; i++)
        delCookie(cookieNames[i])
}

function gaOptout() {
    document.cookie = disableStr + '=true;'+ getCookieExpireDate() +' ; path=/';
    document.cookie = 'hasConsent=false;'+ getCookieExpireDate() +' ; path=/';

    alert('Vous vous êtes opposé au dépôt de cookies de mesures d’audience dans votre navigateur.');

    window[disableStr] = true;
    deleteAnalyticsCookies();
}

function gaOk() {
    document.cookie = 'hasConsent=true; '+ getCookieExpireDate() +' ; path=/'; 

    var div = document.getElementById('cookie-banner');
    if (div != null) div.style.visibility = 'hidden'
}

var consentCookie =  getCookie('hasConsent');
if (!consentCookie) {
 var referrer_host = document.referrer.split('/')[2]; 
   if ( referrer_host != document.location.hostname ) {
     window[disableStr] = true;
     window[disableStr] = true;
     window.onload = askConsent;
   } else {
      document.cookie = 'hasConsent=true; '+ getCookieExpireDate() +' ; path=/'; 
   }
}
