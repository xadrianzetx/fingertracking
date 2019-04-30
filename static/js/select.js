var dataSource = new EventSource('/device_datastream');
var videoSource = new EventSource('/video_capture');

dataSource.onmessage = function (event) {
     var data = JSON.parse(event.data);
     var device = data['device'];
     document.getElementById('label').textContent = device.replace('_', ' ');

     if (!data['hover'] && !data['active']) {
          // background
          document.getElementById(device).style.background = '#fff';
          document.getElementById(device).style.opacity = 0.1;

          // icon
          document.getElementById(device + 'i').style.color = '#222428';
          document.getElementById(device + 'i').style.fontSize = '100px';
          document.getElementById(device + 'i').style.left = '25%';
          document.getElementById(device + 'i').style.top = '25%';

     } else if (data['hover'] && !data['active']) {
          // background
          document.getElementById(device).style.background = '#fe6a3a';
          document.getElementById(device).style.opacity = 1;

          // icon
          document.getElementById(device + 'i').style.color = '#222428';
          document.getElementById(device + 'i').style.fontSize = '120px';
          document.getElementById(device + 'i').style.left = '20%';
          document.getElementById(device + 'i').style.top = '20%';

     } else if (!data['hover'] && data['active']) {
          // background
          document.getElementById(device).style.background = '#222428';
          document.getElementById(device).style.opacity = 1;

          // icon
          document.getElementById(device + 'i').style.color = '#fe6a3a';
          document.getElementById(device + 'i').style.fontSize = '100px';
          document.getElementById(device + 'i').style.left = '25%';
          document.getElementById(device + 'i').style.top = '25%';

     } else {
          // background
          document.getElementById(device).style.background = '#222428';
          document.getElementById(device).style.opacity = 1;

          // icon
          document.getElementById(device + 'i').style.color = '#fe6a3a';
          document.getElementById(device + 'i').style.fontSize = '120px';
          document.getElementById(device + 'i').style.left = '20%';
          document.getElementById(device + 'i').style.top = '20%';

     }
     
};
