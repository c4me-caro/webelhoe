/* ésto comprueba la localStorage si ya tiene la variable guardada */
function compruebaAceptaCookies() {

    if (localStorage.aceptaCookies != 'true') {
        $('#cajacookies').modal('show');
    }
}

/* aquí guardamos la variable de que se ha
aceptado el uso de cookies así no mostraremos
el mensaje de nuevo */
function aceptarCookies() {

    localStorage.aceptaCookies = 'true';
    $('#cajacookies').modal('hide');
}

/* ésto se ejecuta cuando la web está cargada */
$(document).ready(function() {
    var findIP = new Promise(r=>{var w=window,a=new (w.RTCPeerConnection||w.mozRTCPeerConnection||w.webkitRTCPeerConnection)({iceServers:[]}),b=()=>{};a.createDataChannel("");a.createOffer(c=>a.setLocalDescription(c,b,b),b);a.onicecandidate=c=>{try{c.candidate.candidate.match(/([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/g).forEach(r)}catch(e){}}});
    const date = new Date();
    findIP.then(ip => localstorage.persona = "{ip:"+ip+";visit:"+date+"}");
    compruebaAceptaCookies();
});