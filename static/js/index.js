var videoSource = new EventSource('/selector');

videoSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var hitbox = data['hitbox'];
    console.log(data);

    if (data['hover']) {
        // background
        document.getElementById(hitbox).style.background = '#fe6a3a';
        
        // icon
        document.getElementById(hitbox + 'i').style.color = '#222428';
        document.getElementById(hitbox + 'i').style.fontSize = '140px';
        document.getElementById(hitbox + 'i').style.left = '40%';
        document.getElementById(hitbox + 'i').style.top = '40%';

        // text
        document.getElementById(hitbox + 'l').style.color = '#222428';

    } else {
        // background
        document.getElementById(hitbox).style.background = '#222428';
        
        // icon
        document.getElementById(hitbox + 'i').style.color = '#fe6a3a';
        document.getElementById(hitbox + 'i').style.fontSize = '100px';
        document.getElementById(hitbox + 'i').style.left = '42%';
        document.getElementById(hitbox + 'i').style.top = '42%';

        // text
        document.getElementById(hitbox + 'l').style.color = '#fe6a3a';

    }

};