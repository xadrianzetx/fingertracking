var videoSource = new EventSource('/motion_tracking');

var icons = {
    'volume_up': 'fas fa-volume-up',
    'volume_down': 'fas fa-volume-down',
    'swipe_left': 'fas fa-caret-left',
    'swipe_right': 'fas fa-caret-right',
    'scroll_up': 'fas fa-caret-up',
    'scroll_down': 'fas fa-caret-down'
}

videoSource.onmessage = function(event) {
    var data = JSON.parse(event.data);
    
    if (data['active'] != null) {
        var active = [ ...new Set(data['active']) ]

        for (var i = 0; i < active.length; i++) {
            var location = active[i].toString()
            document.getElementById('a_' + location).style.background = '#fe6a3a';
            document.getElementById('a_' + location).style.opacity = 1;
        }

    } else {
        var locations = ['a_0', 'a_1', 'a_2', 'a_3']

        for (var i = 0; i < locations.length; i++) {
            document.getElementById(locations[i]).style.background = '#fff';
            document.getElementById(locations[i]).style.opacity = 0.1;
        }

        if (data['move'] != null) {
            var icon = icons[data['move']];
            var label = data['move'].replace('_', ' ');

            document.getElementById('cover_i').className = icon;
            document.getElementById('cover_l').textContent = label;
        }

    }
    
}