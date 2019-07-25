var args = require('system').args;
var page = require('webpage').create();
page.settings.loadImages = false;
page.settings.resourceTimeout = 5000;
var fs = require('fs');
var currPath = fs.workingDirectory
var address = args[1];
var requestsArray = [];
var url = address;
var postFile = ''

if (fs.exists(currPath+'/js/post.txt')){
    postFile = currPath+'/js/post.txt'
}
else if (fs.exists(currPath+'/post.txt')){
    postFile = currPath+'/post.txt'
}
else{
    console.log("path not current");
    console.log("post.txt not exit");
    phantom.exit();
}

page.open(url, function() {
    //var rawText = "123123124124@gmail.com";
    var rawText = page.content;
    var matches = rawText.match(/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}/)
    console.log("********************************************************************");
    console.log(matches);
    console.log(rawText);
    //console.log(page.plainText)
    clearFile();
    clickType();
    getGet();
    getForm();
    getEmail();
	var interval = setInterval(function () {
    if (requestsArray.length === 0) {
          clearInterval(interval);
          phantom.exit();
    	}
 	}, 1);
});

page.onResourceRequested = function(request, networkRequest) {
    requestsArray.push(request.id);
    url = JSON.parse(JSON.stringify(request, undefined, 4)).url;
    data = JSON.parse(JSON.stringify(request, undefined, 4)).postData;
    if(data){ 
        head = JSON.parse(JSON.stringify(request, undefined, 4)).headers;
        var hostv = parseURL(request.url).domain;
        var addHost = {"name":"Host", "value":hostv}
        var addConn = {"name":"Connection", "value":"keep-alive"}
        var addLang = {"name":"Accept-Language", "value":"en-US,en;q=0.5"}
        var addEnco = {"name":"Accept-Encoding", "value":"gzip,deflate,br"}
        head.push(addHost)
        head.push(addConn)
        head.push(addLang)
        head.push(addEnco)
        if (!(url.indexOf('.js') > -1 || url.indexOf('.css') > -1)){
            re_obj2 = {"url":url,"data":data, "headers":head};
            console.log(url);
            //console.log(data);
            fs.write(postFile, JSON.stringify(re_obj2)+"\n", 'a');
        }
    }
    else{
        if (!(url.indexOf('.js') > -1 || url.indexOf('.css') > -1)){
            console.log(url)
        }
    }
};

page.onResourceReceived = function(response) {
  var index = requestsArray.indexOf(response.id);
  requestsArray.splice(index, 1); 
};

page.onResourceTimeout = function(e) {
  console.log("timeout-----------" + e.url);         // the url whose request timed out
};

function clearFile(){
    fs.write(postFile, "", 'w');
}

//parse url
function parseURL(url){
    parsed_url = {}

    if ( url == null || url.length == 0 )
        return parsed_url;
    protocol_i = url.indexOf('://');
    parsed_url.protocol = url.substr(0,protocol_i);
    remaining_url = url.substr(protocol_i + 3, url.length);
    domain_i = remaining_url.indexOf('/');
    domain_i = domain_i == -1 ? remaining_url.length - 1 : domain_i;
    parsed_url.domain = remaining_url.substr(0, domain_i);
    parsed_url.path = domain_i == -1 || domain_i + 1 == remaining_url.length ? null : remaining_url.substr(domain_i + 1, remaining_url.length);
    domain_parts = parsed_url.domain.split('.');
    switch ( domain_parts.length ){
        case 2:
          parsed_url.subdomain = null;
          parsed_url.host = domain_parts[0];
          parsed_url.tld = domain_parts[1];
          break;
        case 3:
          parsed_url.subdomain = domain_parts[0];
          parsed_url.host = domain_parts[1];
          parsed_url.tld = domain_parts[2];
          break;
        case 4:
          parsed_url.subdomain = domain_parts[0];
          parsed_url.host = domain_parts[1];
          parsed_url.tld = domain_parts[2] + '.' + domain_parts[3];
          break;
    }
    parsed_url.parent_domain = parsed_url.host + '.' + parsed_url.tld;
    return parsed_url;
}

//Get input tag click
function clickType(){
	page.evaluate(function () {
        var tmp = document.getElementsByTagName('input');
        for(var i=0; i < tmp.length; i++){
            if(tmp[i].type=="button" || tmp[i].type=="submit"){
                tmp[i].click();
            }
        }
    });

}

//Get parent link
function getGet(){
    var parent = page.evaluate(function() {
        var test = document.querySelectorAll('a');
        return Array.prototype.map.call(test, function(elem) {
            return elem.href;    
        });
    }); 
    for(var i=0; i < parent.length; i++){
        console.log(parent[i]);
        //fs.write('./get.txt', parent[i] +"\n", 'a');
    }
}

//Get form submit
function getForm(){
	page.evaluate(function () {
        for(var i=0; i < document.forms.length; i++){
            document.forms[i].submit()
        }
    });

}
// email
function getEmail(){
    console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyppp")
    console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyppp")
    console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyppp")
    console.log("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyppp")
}

