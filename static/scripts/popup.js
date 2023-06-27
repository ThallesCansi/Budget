function openPopup() {
    var popup = document.getElementById('app-form');
    popup.style.display = 'flex';
}

function openPopupReceita() {
    var popup = document.getElementById('app-form-receita');
    popup.style.display = 'flex';
}

function openPopupDespesa() {
    var popup = document.getElementById('app-form-despesa');
    popup.style.display = 'flex';
}

function openPopupConta() {
    var popup = document.getElementById('app-form-conta');
    popup.style.display = 'flex';
}

function openPopupCategoria() {
    var popup = document.getElementById('app-form-categoria');
    popup.style.display = 'flex';
}

function openPopupExcluir() {
    var popup = document.getElementById('app-form-excluir');
    popup.style.display = 'flex';
}

var count = 0
function openPopupButton() {
    if (count == 0) {
        var popup = document.getElementById('tipoRouD');
        popup.style.display = 'flex';
        count = 1; 
    } else if (count == 1) {    
        var popup = document.getElementById('tipoRouD');
        popup.style.display = 'none';
        count = 0; 
    }
}

function closePopup() {
    var popup = document.getElementById('app-form');
    popup.style.display = 'none';
}

function closePopupReceita() {
    var popup = document.getElementById('app-form-receita');
    popup.style.display = 'none';
}

function closePopupDespesa() {
    var popup = document.getElementById('app-form-despesa');
    popup.style.display = 'none';
}

function closePopupConta() {
    var popup = document.getElementById('app-form-conta');
    popup.style.display = 'none';
}

function closePopupCategoria() {
    var popup = document.getElementById('app-form-categoria');
    popup.style.display = 'none';
}

function closePopupExcluir() {
    var popup = document.getElementById('app-form-excluir');
    popup.style.display = 'none';
}