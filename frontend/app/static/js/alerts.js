alerttemplate=
'<div class="alert ALERT_TYPE alert-dismissible fade show" role="alert" id="ALERT_ID"> \
ALERT_IMAGE\
<strong>ALERT_TITLE</strong> ALERT_MESSAGE\
<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
</div>';

var dangerImage='<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>';
var successImage='<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>';
var warningImage = '<svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>'
var imageMap=
{
    'alert-warning':warningImage,
    'alert-success':successImage,
    'alert-danger':dangerImage
}


function showAlert(div,type,title,message)
{
    var newAlert=alerttemplate;
    alertId  = div.replace('#','')+"AlertBox";
    newAlert = newAlert.replace('ALERT_ID',alertId);
    newAlert = newAlert.replace('ALERT_TYPE',type);
    newAlert = newAlert.replace('ALERT_IMAGE',imageMap[type]); 
    newAlert = newAlert.replace('ALERT_TITLE',title); 
    newAlert = newAlert.replace('ALERT_MESSAGE',message); 
    if ($('#'+alertId).length==0)
        $(div).append(newAlert);
}

function removeAlert(div)
{
    $(div+'AlertBox').remove()
}