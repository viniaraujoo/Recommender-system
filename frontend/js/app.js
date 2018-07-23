'use strict';

function request(url) {
    return fetch(url).then(response => response.json());
}

function get_results(event) {
    let form = document.getElementById('form');
    let movies = document.getElementById('movies');
    let movies2 = document.getElementById('movies2');

    request('/api/results' + `?uid=${form.user.value}`).then(data => {
        let li = "";
        li = data.result.reduce((movies, movie) => {
            return movies + `<li>${movie}</li>`;
        }, li);
        movies.innerHTML = li;

        li = "";
        li = data.result2.reduce((movies, movie) => {
            return movies + `<li>${movie}</li>`;
        }, li);
        movies2.innerHTML = li;
    });
    return false;
}

request('/api/users').then(data => {
    let usersSelect = document.getElementById('users');
    let options = usersSelect.innerHTML;
    options = data.users_id.reduce((options, userId) => {
        return options + `<option value=${userId}>${userId}</option>`;
    }, options);

    usersSelect.innerHTML = options;
});