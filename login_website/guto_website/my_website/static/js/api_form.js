        // Captura o envio do formulário e realiza a busca
        $('#search-form').submit(function(event) {
            event.preventDefault(); // Impede o envio do formulário padrão

            let searchTerm = $('#search-input').val(); // Obtém o termo de busca

            // Realiza a solicitação AJAX para sua view Django
            $.ajax({
                type: 'GET',
                url: '/search-udemy/?query=' + searchTerm,
                success: function(response) {
                    displayResults(response); // Chama a função para exibir os resultados
                },
                error: function(error) {
                    $('#search-results').html('Erro ao buscar cursos na Udemy.');
                }
            });
        });

        // Função para exibir os resultados na página
        function displayResults(results) {
            $('#search-results').empty(); // Limpa os resultados anteriores, se houver

            if (results.error) {
                $('#search-results').html('Erro: ' + results.error);
                return;
            }

            // Exibe os resultados na página
            results.results.forEach(function(course) {
                $('#search-results').append('<p>' + course.title + '</p>');
            });
        }