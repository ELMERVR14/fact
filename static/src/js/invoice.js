$(document).ready(function()
{
   
    setInterval(function(){ 
    var invoice_number = $("span[name=number]").text();
    var firstPart = invoice_number.substring(0, 2);
    if(firstPart=="FC" || firstPart=="FD")
    {
        $("button[name=202]").fadeOut();
    }
    
   }, 1000);
})
 