(function(){

    const cabecalhoNavA = document.querySelectorAll('.cabecalho nav a');
    const [a1, a2] = cabecalhoNavA;

    const cabecalhoOcultoNavA = document.querySelectorAll('.cabecalho-oculto nav a');
    const [a3, a4] = cabecalhoOcultoNavA;

    const skillh2 = document.querySelectorAll('.skill h2');
    const [numero1, numero2, numero3] = skillh2;

    const skillCircle = document.querySelectorAll('.skill circle');
    const [circle1, circle2, circle3, circle4, circle5, circle6] = skillCircle;

    const botoesAmei = document.querySelectorAll('.interacoes img:nth-of-type(1)');
    const botoesCurtida = document.querySelectorAll('.interacoes img:nth-of-type(2)');
    const palavrasCurtida = document.querySelectorAll('.curtir-responder p:nth-of-type(1)');
    const botoesP = document.querySelectorAll('.interacoes p');

    const botoesResponder = document.querySelectorAll('.curtir-responder p:nth-of-type(2)');
    const aviso = document.querySelector('.aviso');
    const botaoAviso = document.querySelector('.aviso span');

    const formularioRecomendacoes = document.querySelector('.formulario-recomendacoes');
    const botaoformularioRecomendacoes = document.querySelector('.formulario-recomendacoes span');
    const avisoRecomendacoesSpan = document.querySelector('.aviso-recomendacoes span');
    const avisoRecomendacoes = document.querySelector('.aviso-recomendacoes');

    const avisoChamada = document.querySelector('.video_chamada');
    const avisoChamadaSpan = document.querySelector('.aviso-video-chamada span');
    const avisoVideoChamada = document.querySelector('.aviso-video-chamada');
    const pedirVideo = document.querySelector('.pedir_video');

    const sorteioParticipar = document.querySelector('.sorteio-participar');
    const formularioSorteio = document.querySelector('.formulario-sorteio');
    const botaoformularioSorteio = document.querySelector('.formulario-sorteio span');
    const avisoSorteioSpan = document.querySelector('.aviso-sorteio span');
    const avisoSorteio = document.querySelector('.aviso-sorteio');


    let contador1 = 0;
    let contador2 = 0;
    let contadorCircle1 = 450;
    let contadorCircle2 = 450;

    let contador3 = 0;
    let contador4 = 0;
    let contadorCircle3 = 450;
    let contadorCircle4 = 450;

    let contador5 = 0;
    let contador6 = 0;
    let contadorCircle5 = 450;
    let contadorCircle6 = 450;

    let intervalo1 = setInterval(function(){
        numero1.innerHTML = contador1;
        contador1 += 8;

        if(contador1 == 248){
            clearInterval(intervalo1);
        }
    }, 100);

    let intervaloCount1 = setInterval(function(){
        circle1.setAttribute('style', `stroke-dashoffset: ${contadorCircle1};`);
        contadorCircle1--;

        if(contadorCircle1 == 50){
            clearInterval(intervaloCount1);
        }
    }, 1);

    let intervaloCount2 = setInterval(function(){
        circle2.setAttribute('style', `stroke-dashoffset: ${contadorCircle2};`);
        contadorCircle2--;

        if(contadorCircle2 == 230){
            clearInterval(intervaloCount2);
        }
    }, 10);


    let intervalo3 = setInterval(function(){
        numero2.innerHTML = contador3;
        contador3 += 1000;

        if(contador3 == 50000){
            clearInterval(intervalo3);
        }
    }, 50);

    let intervaloCount3 = setInterval(function(){
        circle3.setAttribute('style', `stroke-dashoffset: ${contadorCircle3};`);
        contadorCircle3--;

        if(contadorCircle3 == 100){
            clearInterval(intervaloCount3);
        }
    }, 1);

    let intervaloCount4 = setInterval(function(){
        circle4.setAttribute('style', `stroke-dashoffset: ${contadorCircle4};`);
        contadorCircle4--;

        if(contadorCircle4 == 260){
            clearInterval(intervaloCount4);
        }
    }, 10);


    let intervalo5 = setInterval(function(){
        numero3.innerHTML = contador5;
        contador5 += 15;

        if(contador5 == 495){
            clearInterval(intervalo5);
        }
    }, 30);

    let intervaloCount5 = setInterval(function(){
        circle5.setAttribute('style', `stroke-dashoffset: ${contadorCircle5};`);
        contadorCircle5--;

        if(contadorCircle5 == 150){
            clearInterval(intervaloCount5);
        }
    }, 1);

    let intervaloCount6 = setInterval(function(){
        circle6.setAttribute('style', `stroke-dashoffset: ${contadorCircle6};`);
        contadorCircle6--;

        if(contadorCircle6 == 300){
            clearInterval(intervaloCount6);
        }
    }, 10);

    document.addEventListener('click', e => {

        const el = e.target;
        for (let i = 0; i < botoesAmei.length; i++) {
            if (el == botoesAmei[i] || el == botoesCurtida[i] || el == palavrasCurtida[i]) {
                if (JSON.parse(localStorage.getItem('validador'))) {
                    let numeroCurtida = botoesP[i].innerText;
                    botoesP[i].innerHTML = parseInt(numeroCurtida) + 1;
    
                    if(el == palavrasCurtida[i]){
                        palavrasCurtida[i].innerHTML = 'Descurtir'
                        palavrasCurtida[i].classList.toggle('cinza');
                    }
    
                    botoesAmei[i].classList.toggle('opacidade');
                    botoesCurtida[i].classList.toggle('opacidade');
    
                    localStorage.setItem('validador', JSON.stringify(false))
                } else {
                    let numeroCurtida = botoesP[i].innerText;
                    botoesP[i].innerHTML = parseInt(numeroCurtida) - 1;
    
                    if(el == palavrasCurtida[i]){
                        palavrasCurtida[i].innerHTML = 'Curtir'
                        palavrasCurtida[i].classList.toggle('cinza');
                    }
    
                    botoesAmei[i].classList.toggle('opacidade');
                    botoesCurtida[i].classList.toggle('opacidade');
    
                    localStorage.setItem('validador', JSON.stringify(true))
                }
            }
        }

        if(el == a1 || el == a3){
            e.preventDefault();
            scroll({
                top: 0,
                behavior: 'smooth',
            });
        }

        if(el == a2 || el == a4){
            e.preventDefault();
            scroll({
                top: document.documentElement.scrollHeight,
                behavior: 'smooth',
            });
        }

        for(let botaoResponder of botoesResponder){
            if(botaoAviso == el){
                aviso.classList.remove('aviso_desocultar');
                break;
            }
            if(botaoResponder == el){
                aviso.classList.add('aviso_desocultar');
            }
        }

        if(el == avisoChamada){
            e.preventDefault();
            avisoVideoChamada.classList.add('aviso_desocultar');
            //formularioRecomendacoes.classList.add('aviso_desocultar');
        }

        if(el == avisoChamadaSpan){
            e.preventDefault();
            avisoVideoChamada.classList.remove('aviso_desocultar');
            //formularioRecomendacoes.classList.remove('aviso_desocultar');
        }

        if(el == botaoformularioRecomendacoes){
            formularioRecomendacoes.classList.remove('aviso_desocultar');
            avisoRecomendacoes.classList.add('aviso_desocultar');
        }

        if(el == pedirVideo){
            e.preventDefault();
            formularioRecomendacoes.classList.add('aviso_desocultar');
        }

        if(el == avisoRecomendacoesSpan){
            avisoRecomendacoes.classList.remove('aviso_desocultar');
        }

        if(el == sorteioParticipar){
            e.preventDefault();
            formularioSorteio.classList.add('aviso_desocultar');
        }

        if(el == botaoformularioSorteio){
            formularioSorteio.classList.remove('aviso_desocultar');
            avisoSorteio.classList.add('aviso_desocultar');
        }

        if(el == avisoSorteioSpan){
            avisoSorteio.classList.remove('aviso_desocultar');
        }

    });

})();