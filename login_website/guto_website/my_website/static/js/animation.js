function showLoadingAnimation() {
    $('#loading').show();
}

function hideLoadingAnimation(){
    $('#loading').hide();
}

function executeVerification(){
    showLoadingAnimation();

        $.post('Atualizar_Usuario', function(data){
            hideLoadingAnimation();
        });
}

$('#botao_atualizar').click(function(){
    executeVerification();
})