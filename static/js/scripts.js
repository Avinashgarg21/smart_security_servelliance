setInterval(function() {
    fetch('/')
    .then(response => response.text())
    .then(data => {
        document.querySelector('#uploads-list').innerHTML = new DOMParser().parseFromString(data, 'text/html').querySelector('#uploads-list').innerHTML;
    });
}, 5000);
