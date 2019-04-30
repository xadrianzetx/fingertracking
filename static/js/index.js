var videoSource = new EventSource('/selector');

videoSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    var hitbox = data['hitbox'];

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
        var hitboxes = ['hitbox_l', 'hitbox_r']

        for (var i = 0; i < hitboxes.length; i++) {
            // background
            document.getElementById(hitboxes[i]).style.background = '#222428';
        
            // icon
            document.getElementById(hitboxes[i] + 'i').style.color = '#fe6a3a';
            document.getElementById(hitboxes[i] + 'i').style.fontSize = '100px';
            document.getElementById(hitboxes[i] + 'i').style.left = '42%';
            document.getElementById(hitboxes[i] + 'i').style.top = '50%';

            // text
            document.getElementById(hitboxes[i] + 'l').style.color = '#fe6a3a';

        }

    }

    if (data['fl'] > 10) {
        window.location.href = "/device_select";

    } else if (data['fr'] > 10) {
        window.location.href = "/device_settings";

    }

};