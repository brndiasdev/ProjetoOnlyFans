(function(){
    const metricaVisualizacoes = document.querySelector('.metrica-visualizacoes h2');
    const metricaCurtidas = document.querySelector('.metrica-curtidas h2');

    let curtidas = 2000;
    let visualizacoes = 50000;

    let visualizacoesInterval = setInterval(function(){
        metricaVisualizacoes.innerHTML = visualizacoes.toLocaleString('pt-BR');
        if(visualizacoes == 254382){
            clearInterval(visualizacoesInterval);
        }
        visualizacoes+=1
    }, 0.01);

    let curtidasInterval = setInterval(function(){
        metricaCurtidas.innerHTML = curtidas.toLocaleString('pt-BR');
        if(curtidas == 12453){
            clearInterval(curtidasInterval);
        }
        curtidas+=1
    }, 100);

})();