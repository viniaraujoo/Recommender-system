let hello = document.getElementById('hello');

fetch('/api/hello')
    .then(response => response.json())
    .then(json => hello.innerText = json.msg);