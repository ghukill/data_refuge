function filterXSS(ele) {
    var display = ele;
    var description = ele.value;
    if(description != undefined)
    {
        description.replace(/[\"\'][\s]*javascript:(.*)[\"\']/g, "\"\"");
        description = description.replace(/script(.*)/g, "");    
        description = description.replace(/eval\((.*)\)/g, "");
        description = description.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        display.value = description;
       }
  } 
 
//Get the x,y position of any element on a page.
//see this URL for more information: http://vishalsays.wordpress.com/2007/12/21/finding-elements-top-and-left-using-javascript/
function GetTopLeft(elm)

{

var x, y = 0;

//set x to elm’s offsetLeft
x = elm.offsetLeft;

//set y to elm’s offsetTop
y = elm.offsetTop;

//set elm to its offsetParent
elm = elm.offsetParent;

//use while loop to check if elm is null
// if not then add current elm’s offsetLeft to x
//offsetTop to y and set elm to its offsetParent

while(elm != null)
{

x = parseInt(x) + parseInt(elm.offsetLeft);
y = parseInt(y) + parseInt(elm.offsetTop);
elm = elm.offsetParent;
}

//here is interesting thing
//it return Object with two properties
//Top and Left

return {Top:y, Left: x};

}

//popup a new window. See this URL for more info: http://forums.htmlcenter.com/usability-accessability/613-dont-open-new-windows-target-_blank.html
var newWindow = null;

function closeWin(){
if (newWindow != null){
if(!newWindow.closed)
newWindow.close();
}
}

function popUpWin(url, type, strWidth, strHeight){

closeWin();

if (type == "fullScreen"){

strWidth = screen.availWidth - 10;
strHeight = screen.availHeight - 160;
}

var tools="";
if (type == "standard" || type == "fullScreen") tools = "resizable,toolbar=yes,location=yes,scrollbars=yes ,menubar=yes,width="+strWidth+",height="+strHeight +",top=0,left=0";
if (type == "console") tools = "resizable,toolbar=no,location=no,scrollbars=no,width="+strWidth+",height="+strHeight+",left=0,top=0 ";
newWindow = window.open(url, 'newWin', tools);
newWindow.focus();
}

function set_printable_version()
    {
    //Sets the querystring for the printable version links
    
    if (window.location.search.substring(1) != '') {
        var printlink = document.getElementById("printversion");
        var querystring = window.location.search.substring(1);
        
        querystring = querystring.replace('>', '');
        querystring = querystring.replace('<', '');
        printlink.href = printlink.href + '?' + querystring;
    }//end if
    }

function toProperCase(s)
{
  return s.toLowerCase().replace(/^(.)|\s(.)/g, 
          function($1) { return $1.toUpperCase(); });
}

function formatNumber(number,decimalplace)
{
    number = number.toFixed(decimalplace) + '';
    x = number.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}

 (function() {
    var hst = window.location.hostname;

    if (hst != "www2.eere.energy.gov") {
        var so = document.createElement('script'); so.type = 'text/javascript'; so.async = true;
        so.src = '//www.eere.energy.gov/includes/ga/eere.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(so, s);
    }
  })();
