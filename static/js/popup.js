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
