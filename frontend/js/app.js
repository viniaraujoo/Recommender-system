(function() {
    'use strict';
    const form = document.getElementById('form');

    function request(url) {
        return fetch(url).then(response => response.json());
    }

    function change_list_content(list, element) {
        const li = list.reduce((elements, value) => {
            return elements + `<li>${value}</li>`;
        }, "");
        element.innerHTML = li;
    }

    function change_explication_content(neighbors) {
        const explication_text = document.getElementById('explication_text');
        const neighbors_element = document.getElementById('neighbors');
        const explication = "Essa recomendações de filmes é de acordo "
                        + "com a nota que outros usuários que tem perfis "
                        + "similares a este perfil, atribuiram aos filmes escolhidos. "
                        + "Os filmes recomendados são os que possuem as maiores notas "
                        + "atribuidas por estes 5 usuários com perfis mais similares: ";
        
        explication_text.innerText = explication;
        change_list_content(neighbors, neighbors_element);
    }

    function get_results() {
        const movies_knn = document.getElementById('movies_knn');
        const movies_svd = document.getElementById('movies_svd');

        request(`/api/results?uid=${form.user.value}`).then(data => {
            change_list_content(data.result_knn, movies_knn);
            change_list_content(data.result_svd, movies_svd);
            change_explication_content(data.neighbors);
        });
        return false;
    }


    (function main() {
        form.onsubmit = get_results;
        request('/api/users').then(data => {
            const usersSelect = document.getElementById('users');
            const options = data.users_id.reduce((options, userId) => {
                return options + `<option value=${userId}>${userId}</option>`;
            }, usersSelect.innerHTML);

            usersSelect.innerHTML = options;
        });
    })();
})();