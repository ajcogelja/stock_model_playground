var data = null
var init = false;
json_file = ''

async function readTextFile() {
    //console.log('json file: ', json_file);
    // var rawFile = new XMLHttpRequest();
    // rawFile.overrideMimeType("application/json");
    // rawFile.open("GET", file, true);
    // rawFile.onreadystatechange = function() {
    //     if (rawFile.readyState === 4 && rawFile.status == "200") {
    //         initialize_callback(rawFile.responseText);
    //     }
    // }
    // rawFile.send(null);
    // const url = 'https://s3.us-east-2.amazonaws.com/ajc.champ.bucket/champs.json'
    // try{
    //     const fetchResp = await fetch(url, {
    //         headers: {
    //             'method': 
    //         }
    //     });
    //     return await fetchResp.json()
    // } catch (err){
    //     console.log('error ', err);
    // }
    // const xhr = new XMLHttpRequest();
    // const url = 'https://s3.us-east-2.amazonaws.com/ajc.champ.bucket/champs.json'
    // xhr.open('GET', url);
    // xhr.setRequestHeader('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    // xhr.setRequestHeader('Sec-Fetch-Dest', 'document')
    // xhr.setRequestHeader('Sec-Fetch-Mode', 'navigate')
    // xhr.setRequestHeader('Sec-Fetch-Site', 'same-origin')
    // xhr.setRequestHeader('Sec-Fetch-User', '?1')
    // xhr.onreadystatechange = (handle) => {
    //     console.log('handle: ', handle)
    // };
    // xhr.send();
}

var createCORSRequest = function(method, url) {
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr) {
      // Most browsers.
      xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined") {
      // IE8 & IE9
      xhr = new XDomainRequest();
      xhr.open(method, url);
    } else {
      // CORS not supported.
      xhr = null;
    }
    return xhr;
  };
  
function loadData(){
    console.log('start data load')
    var url = 'https://s3.us-east-2.amazonaws.com/ajc.champ.bucket/champs.json';
    var method = 'GET';
    var xhr = createCORSRequest(method, url);
    xhr.send();
    xhr.onreadystatechange = function(res) {
        if(xhr.readyState == XMLHttpRequest.DONE){
            console.log('res: ', res)
            init = true
            console.log('success: ', xhr.response)
            data = JSON.parse(xhr.responseText)
            console.log('data: ', data)
            xhr.onreadystatechange = () => {}
        }
        // Success code goes here.
      };
      
      xhr.onerror = function(err) {
        // Error code goes here.
        console.log('failure', err)
      };
    
}

  
  

function initialize(){
    readTextFile()
    console.log('data:', data);
}

function check_init(){
    if(!init){
        console.log('not initialized yet!')
    }
    return data != null && init
}

function check_champ(name){
    console.log('og name: ', name)
    name = document.getElementById('champ_one_name').value
    console.log('clicked: ', name);
    if(!check_init()){
        return false;
    }
    //var name = 
    if(Object.keys(data).includes(name)){
        console.log('it is a champ name: ', name);
        return true;
    } else {
        console.log('name not in keys: ', name)
        return false;
    }

}
//usage:
//     data = JSON.parse(text);
//     init = true
// });

// while(!init){
//     setTimeout(() => {}, 500)
//     console.log('trying again!');
// }