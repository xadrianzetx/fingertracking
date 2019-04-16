var dataSource = new EventSource('/stream');
var videoSource = new EventSource('/video_capture');

dataSource.onmessage = function (event) {
     var data = JSON.parse(event.data);
     
     document.getElementById('device').textContent = data['device'];
     document.getElementById("hover").textContent = data['hover'];
     document.getElementById('active').textContent = data['active'];
};
