$(document).ready(function () {
    // Ao enviar o formulário
    $("#atualizar-form").submit(function (event) {
        event.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                $("#nome-value").text(data.nome);
                $("#descricao").text(data.descricao);
                $("#mensagem").text("Dados atualizados com sucesso, caso não a página não reflita as mudanças, por-favor recarregue a página");
            },
            error: function () {
                $("#mensagem").text("Erro ao atualizar os dados.");
            }
        });
    });
});

document.getElementById('mostrarOpcoes').addEventListener('click', function (){
    var opcoes = document.getElementById('opcoesAlteracao');
    if (opcoes.style.display === 'none' || opcoes.style.display === ''){
        opcoes.style.display = 'block';
    } else {
        opcoes.style.display = 'none';
    }
});