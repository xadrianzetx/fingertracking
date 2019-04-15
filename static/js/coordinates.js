var source = new EventSource('/stream');

source.onmessage = function (event) {
     console.log(event.data);
};