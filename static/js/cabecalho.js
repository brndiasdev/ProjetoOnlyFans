(function(){

    const cabecalhoOculto = document.querySelector('.cabecalho-oculto');
    const botaoOculto = document.querySelector('.botao-oculto');
    const botaoOcultoSpan = document.querySelectorAll('.botao-oculto span');
    const [span1, span2] = botaoOcultoSpan;

    const botaoMobile = document.querySelector('.botao-mobile');
    const botaoMobileSpan = document.querySelectorAll('.botao-mobile span');
    const [span3, span4, span5] = botaoMobileSpan;

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botaoOculto || el == span1 || el == span2){
            cabecalhoOculto.classList.remove('cabecalho-oculto-mostrar');
        } 
        if(el == botaoMobile || el == span3 || el == span4 || el == span5){
            cabecalhoOculto.classList.add('cabecalho-oculto-mostrar');
        }
    
    });

})();