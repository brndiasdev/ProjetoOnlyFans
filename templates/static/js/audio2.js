(function(){

    const botaoPlayer = document.querySelector('#audio2 .imagem-play');
    const botaoPause = document.querySelector('#audio2 .imagem-pause');
    const playerAudio = document.querySelector('#audio2 #player');
    const barraProgresso1 = document.querySelector('#audio2 .progresso>div:nth-child(1)');
    const barraProgresso2 = document.querySelector('#audio2 .progresso>div:nth-child(1)>div');
    const contadorProgresso = document.querySelector('#audio2 .progresso>p:nth-of-type(1)');

    let musica = true;
    playerAudio.src = "/static/audios/audio2.mp3";

    document.addEventListener('click', e => {

        const el = e.target;

        if(el == botaoPlayer || el == botaoPause){
            if(!musica){
                playerAudio.pause();
                botaoPlayer.classList.remove('botao-esconder');
                botaoPause.classList.remove('botao-mostrar');
                musica = true;
            } else{
                playerAudio.play();
                botaoPlayer.classList.add('botao-esconder');
                botaoPause.classList.add('botao-mostrar');
                musica = false;
                let intervaloContador = setInterval(function(){
                    updateTime();
                    if(playerAudio.currentTime == playerAudio.duration){
                        clearInterval(intervaloContador);
                    }
                }, 1000);
            }
        }

        if(el == barraProgresso1 || el == barraProgresso2){
            const newTime = (e.offsetX / el.offsetWidth) * playerAudio.duration;
            playerAudio.currentTime = newTime;
        }

    });

    const formataZero = (n) => (n < 10 ? '0' + n : n);

    function updateTime(){
        const currentMinutes = Math.floor(playerAudio.currentTime / 60);
        const currentSeconds = Math.floor(playerAudio.currentTime % 60);
        contadorProgresso.innerHTML = currentMinutes + ':' + formataZero(currentSeconds);

        const durationFormated = isNaN(playerAudio.duration) ? 0 : playerAudio.duration;
        /* const durationMinutes = Math.floor(durationFormated / 60);
        const durationSeconds = Math.floor(durationFormated % 60); */
        const progressWidth = durationFormated
            ? (playerAudio.currentTime / durationFormated) * 100 : 0;

            barraProgresso2.style.width = progressWidth + '%';
    }

})();