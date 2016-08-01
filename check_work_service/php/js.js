var classlist = document.getElementsByClassName("weui_cell")

function getURL(url) {
        var xmlhttp = new ActiveXObject( "Microsoft.XMLHTTP");
        xmlhttp.open("GET", url, false);
        xmlhttp.send();
        if(xmlhttp.readyState==4) {
            if(xmlhttp.Status != 200) alert("不存在");
            return xmlhttp.Status==200;
        }
        return false;
}