function calcularTamanhoDaTelaMenosElemento() {
    const larguraDaTela = window.innerWidth;
    const larguraDoElemento = document.getElementById('sidebar').offsetWidth;
    const tamanhoDaTelaMenosElemento = larguraDaTela - larguraDoElemento;
    const amais = 50

    // Aplicar a largura calculada à navbar
    document.getElementById('navbar').style.width = tamanhoDaTelaMenosElemento + amais + 'px';
    }

    // Chame a função após a carga completa da página
    window.addEventListener('load', calcularTamanhoDaTelaMenosElemento);

    // Adicione um evento de redimensionamento para recalcular quando a janela for redimensionada
    window.addEventListener('resize', calcularTamanhoDaTelaMenosElemento);