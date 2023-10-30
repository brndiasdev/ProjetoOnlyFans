(function(){

    const inputCartao = document.querySelector('#cartao');
    const divCartao = document.querySelector('form .cartao');

    $(document).ready(function() {
        $("#numero-cartao").mask("0000 0000 0000 0000");
        $("#data-expiracao").mask("00/00");
        $("#codigo-cartao").mask("000");
    });

    document.addEventListener('change', e => {

        const el = e.target;
        if(inputCartao.checked){
            divCartao.classList.add('cartao-aparecer');
        } else if(!inputCartao.checked){
            divCartao.classList.remove('cartao-aparecer');
        }

    });

})();